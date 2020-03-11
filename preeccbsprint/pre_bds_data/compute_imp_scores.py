#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import momma_dragonn
from momma_dragonn.data_loaders.pyfasta_data_loader import SingleStreamSeqOnly
import numpy as np
import gzip
import deeplift
from deeplift.conversion import kerasapi_conversion as kc
from deeplift import dinuc_shuffle
import tensorflow as tf
import h5py
import time


fasta_data_source =\
    "/mnt/data/annotations/by_organism/human/hg19.GRCh37/hg19.genome.fa"
argmax_to_letter = {0:'A', 1:'C', 2:'G', 3:'T'}
def onehot_to_seq(onehot):
    seq = "".join([argmax_to_letter[x] for x in np.argmax(onehot,axis=-1)])
    return seq

def one_hot_encode_along_channel_axis(sequence):
    to_return = np.zeros((len(sequence),4), dtype=np.int8)
    seq_to_one_hot_fill_in_array(zeros_array=to_return,
                                 sequence=sequence, one_hot_axis=1)
    return to_return

def seq_to_one_hot_fill_in_array(zeros_array, sequence, one_hot_axis):
    assert one_hot_axis==0 or one_hot_axis==1
    if (one_hot_axis==0):
        assert zeros_array.shape[1] == len(sequence)
    elif (one_hot_axis==1): 
        assert zeros_array.shape[0] == len(sequence)
    #will mutate zeros_array
    for (i,char) in enumerate(sequence):
        if (char=="A" or char=="a"):
            char_idx = 0
        elif (char=="C" or char=="c"):
            char_idx = 1
        elif (char=="G" or char=="g"):
            char_idx = 2
        elif (char=="T" or char=="t"):
            char_idx = 3
        elif (char=="N" or char=="n"):
            continue #leave that pos as all 0's
        else:
            raise RuntimeError("Unsupported character: "+str(char))
        if (one_hot_axis==0):
            zeros_array[char_idx,i] = 1
        elif (one_hot_axis==1):
            zeros_array[i,char_idx] = 1

def list_wrapper(func):
    def wrapped_func(input_data_list, **kwargs):
        if (isinstance(input_data_list, list)):
            remove_list_on_return=False
        else:
            remove_list_on_return=True
            input_data_list = [input_data_list]
        to_return = func(input_data_list=input_data_list,
                         **kwargs)
        return to_return
    return wrapped_func

def empty_ism_buffer(results_arr,
                     input_data_onehot,
                     perturbed_inputs_preds,
                     perturbed_inputs_info):
    for perturbed_input_pred,perturbed_input_info\
        in zip(perturbed_inputs_preds, perturbed_inputs_info):
        example_idx = perturbed_input_info[0]
        if (perturbed_input_info[1]=="original"):
            results_arr[example_idx] +=\
                (perturbed_input_pred*input_data_onehot[example_idx])
        else:
            pos_idx,base_idx = perturbed_input_info[1]
            results_arr[example_idx,pos_idx,base_idx] = perturbed_input_pred

def make_ism_func(prediction_func,
                  flank_around_middle_to_perturb,
                  batch_size=200):
    @list_wrapper
    def ism_func(input_data_list, progress_update=10000, **kwargs):
        assert len(input_data_list)==1
        input_data_onehot=input_data_list[0]
        
        results_arr = np.zeros_like(input_data_onehot).astype("float64")
        
        perturbed_inputs_info = []
        perturbed_onehot_seqs = []
        perturbed_inputs_preds = []
        num_done = 0
        for i,onehot_seq in enumerate(input_data_onehot):
            perturbed_onehot_seqs.append(onehot_seq)
            perturbed_inputs_info.append((i,"original"))
            for pos in range(
                int(len(onehot_seq)/2)-flank_around_middle_to_perturb,
                int(len(onehot_seq)/2)+flank_around_middle_to_perturb):
                for base_idx in range(4):
                    if onehot_seq[pos,base_idx]==0:
                        assert len(onehot_seq.shape)==2
                        new_onehot = np.zeros_like(onehot_seq) + onehot_seq
                        new_onehot[pos,:] = 0
                        new_onehot[pos,base_idx] = 1
                        perturbed_onehot_seqs.append(new_onehot)
                        perturbed_inputs_info.append((i,(pos,base_idx)))
                        num_done += 1
                        if ((progress_update is not None)
                            and num_done%progress_update==0):
                            print("Done",num_done)
                        if (len(perturbed_inputs_info)>=batch_size):
                            empty_ism_buffer(
                                 results_arr=results_arr,
                                 input_data_onehot=input_data_onehot,
                                 perturbed_inputs_preds=
                                  prediction_func([perturbed_onehot_seqs]),
                                 perturbed_inputs_info=perturbed_inputs_info)
                            perturbed_inputs_info = []
                            perturbed_onehot_seqs = []
        if (len(perturbed_inputs_info)>0):
            empty_ism_buffer(
                 results_arr=results_arr,
                 input_data_onehot=input_data_onehot,
                 perturbed_inputs_preds=
                  prediction_func([perturbed_onehot_seqs]),
                 perturbed_inputs_info=perturbed_inputs_info)
        perturbed_inputs_info = []
        perturbed_onehot_seqs = []
        results_arr = results_arr - np.mean(results_arr,axis=-1)[:,:,None]
        return input_data_onehot*results_arr
    return ism_func

def get_project_onto_bases_func(func):
    @list_wrapper
    def project_onto_bases(input_data_list, **kwargs):
        assert len(input_data_list)==1
        to_return = func(input_data_list=input_data_list, **kwargs)
        return input_data_list[0]*np.sum(to_return,axis=-1)[:,:,None]
    return project_onto_bases


def get_scoring_funcs(model_json, model_weights):
    
    deeplift_genomicsdefault_model =\
        kc.convert_model_from_saved_files(
            json_file=model_json,
            h5_file=model_weights,
            nonlinear_mxts_mode=
             deeplift.layers.NonlinearMxtsMode.DeepLIFT_GenomicsDefault) 
    deeplift_rescale_model =\
        kc.convert_model_from_saved_files(
            json_file=model_json,
            h5_file=model_weights,
            nonlinear_mxts_mode=
             deeplift.layers.NonlinearMxtsMode.Rescale) 

    pred_func = deeplift.util.compile_func(
        inputs=[deeplift_genomicsdefault_model.get_layers()[0]
                 .get_activation_vars()],
        outputs=deeplift_genomicsdefault_model.get_layers()[-2]
                 .get_activation_vars()[:,0])

    grad = tf.gradients(
        ys=deeplift_genomicsdefault_model.get_layers()
            [-2].get_activation_vars(),
        xs=deeplift_genomicsdefault_model.get_layers()
            [0].get_activation_vars())[0]
    unbatched_grad_func = deeplift.util.compile_func(
        inputs=[deeplift_genomicsdefault_model.get_layers()[0]
                .get_activation_vars()],
        outputs=grad)

    @list_wrapper
    def grad_func(input_data_list, input_references_list, task_idx, **kwargs):
        assert len(input_data_list)==1
        to_return = np.array(deeplift.util.run_function_in_batches(
                        unbatched_grad_func,
                        input_data_list=input_data_list,
                        **kwargs))
        return to_return

    @list_wrapper
    def grad_times_inp_func(input_data_list, **kwargs):
        assert len(input_data_list)==1
        print("Ignoring reference for grad*input")
        grads = grad_func(input_data_list=input_data_list, **kwargs)
        return grads*input_data_list[0]

    ism_func = make_ism_func(prediction_func=pred_func,
                             flank_around_middle_to_perturb=150,
                             batch_size=200)

    #Flat reference functions
    deeplift_genomicsdefault_contribs_func = get_project_onto_bases_func(
        deeplift_genomicsdefault_model.get_target_contribs_func(
         find_scores_layer_idx=0))
    deeplift_rescale_contribs_func = get_project_onto_bases_func(
        deeplift_rescale_model.get_target_contribs_func(
         find_scores_layer_idx=0))

    intgrad2_func = get_project_onto_bases_func(
        deeplift.util.get_integrated_gradients_function(
        gradient_computation_function=grad_func, 
        num_intervals=2))
    intgrad5_func = get_project_onto_bases_func(
        deeplift.util.get_integrated_gradients_function(
        gradient_computation_function=grad_func, 
        num_intervals=5))
    intgrad10_func = get_project_onto_bases_func(
        deeplift.util.get_integrated_gradients_function(
        gradient_computation_function=grad_func, 
        num_intervals=10))
    intgrad20_func = get_project_onto_bases_func(
        deeplift.util.get_integrated_gradients_function(
        gradient_computation_function=grad_func, 
        num_intervals=20))

    #Dinuc shuff functions
    deeplift_genomicsdefault_dinucshuff_scoringfunc =\
        deeplift.util.get_shuffle_seq_ref_function(
            score_computation_function=
             deeplift_genomicsdefault_contribs_func,
            shuffle_func=deeplift.dinuc_shuffle.dinuc_shuffle,
            one_hot_func=lambda x: np.array(
             [one_hot_encode_along_channel_axis(y) for y in x]))

    deeplift_rescale_dinucshuff_scoringfunc =\
        deeplift.util.get_shuffle_seq_ref_function(
            score_computation_function=deeplift_rescale_contribs_func,
            shuffle_func=deeplift.dinuc_shuffle.dinuc_shuffle,
            one_hot_func=lambda x: np.array(
             [one_hot_encode_along_channel_axis(y) for y in x]))

    intgrad2_dinucshuff_scoringfunc =\
        deeplift.util.get_shuffle_seq_ref_function(
            score_computation_function=intgrad2_func,
            shuffle_func=deeplift.dinuc_shuffle.dinuc_shuffle,
            one_hot_func=lambda x: np.array(
                [one_hot_encode_along_channel_axis(y) for y in x]))
    intgrad5_dinucshuff_scoringfunc =\
        deeplift.util.get_shuffle_seq_ref_function(
            score_computation_function=intgrad5_func,
            shuffle_func=deeplift.dinuc_shuffle.dinuc_shuffle,
            one_hot_func=lambda x: np.array(
                [one_hot_encode_along_channel_axis(y) for y in x]))
    intgrad10_dinucshuff_scoringfunc =\
        deeplift.util.get_shuffle_seq_ref_function(
            score_computation_function=intgrad10_func,
            shuffle_func=deeplift.dinuc_shuffle.dinuc_shuffle,
            one_hot_func=lambda x: np.array(
                [one_hot_encode_along_channel_axis(y) for y in x]))
    intgrad20_dinucshuff_scoringfunc =\
        deeplift.util.get_shuffle_seq_ref_function(
            score_computation_function=intgrad20_func,
            shuffle_func=deeplift.dinuc_shuffle.dinuc_shuffle,
            one_hot_func=lambda x: np.array(
                [one_hot_encode_along_channel_axis(y) for y in x]))
        
    method_name_to_scoring_func = {
         'ism': ism_func,
         'grad_times_inp': grad_times_inp_func,
         'integrated_grad2': intgrad2_func,
         'integrated_grad5': intgrad5_func,
         'integrated_grad10': intgrad10_func,
         'integrated_grad20': intgrad20_func,
         'deeplift_genomicsdefault':
           deeplift_genomicsdefault_contribs_func,
         'deeplift_rescale': deeplift_rescale_contribs_func,
         'deeplift_genomicsdefault_dinucshuff':
           deeplift_genomicsdefault_dinucshuff_scoringfunc,
         'deeplift_rescale_dinucshuff':
           deeplift_rescale_dinucshuff_scoringfunc,
         'integrated_grad2_dinucshuff': intgrad5_dinucshuff_scoringfunc,
         'integrated_grad5_dinucshuff': intgrad5_dinucshuff_scoringfunc,
         'integrated_grad10_dinucshuff': intgrad10_dinucshuff_scoringfunc,
         'integrated_grad20_dinucshuff': intgrad20_dinucshuff_scoringfunc}

    return pred_func, method_name_to_scoring_func


def compute_imp_scores(options):

    if (os.path.isfile("positive_test_examples.gz")):
        data_loader =\
            SingleStreamSeqOnly(
                batch_size=50, bed_source="positive_test_examples.gz",
                fasta_data_source=fasta_data_source, rc_augment=False,
                randomize_after_pass=False, num_to_load_for_eval=None)
        onehot_data = data_loader.get_data().X
        data_seqs = [onehot_to_seq(x) for x in onehot_data]
    else:
        data_seqs = [x.rstrip().split("\t")[4] for
                    x in gzip.open("test_set_positives.bed.gz", "rb")]
        onehot_data = np.array([one_hot_encode_along_channel_axis(x)
                                for x in data_seqs]) 

    for model_id in options.model_ids:

        model_json = "model_files/"+model_id+"_modelJson.json"
        model_weights = "model_files/"+model_id+"_modelWeights.h5"

        pred_func, method_name_to_scoring_func = get_scoring_funcs(
            model_json=model_json, model_weights=model_weights) 

        data_preds =\
            np.array(deeplift.util.run_function_in_batches(
                        pred_func,
                        input_data_list=[onehot_data],
                        batch_size=200,
                        progress_update=10000))

        print("Prediction under all zero input",
              pred_func([np.zeros((1,1000,4))]))
        avg_gcref = np.mean(onehot_data, axis=0, keepdims=True)
        print("Prediction under avg input",
              pred_func([avg_gcref]))

        ####
        #Prepare the subset to score, and score them
        ####
        #sorted_prediction_indices = [
        #  x[0] for x in sorted(enumerate(data_preds),
        #  key=lambda x: -x[1])]
        #subset_indices = sorted_prediction_indices[::10]
        subset_indices = list(range(len(data_preds)))[::options.subsample_rate]
        print("Num to score",len(subset_indices))
        subset_preds =\
            np.array([data_preds[i] for i in subset_indices])
        subset_onehot =\
            np.array([onehot_data[i] for i in subset_indices])
        subset_seqs = [data_seqs[i] for i in subset_indices]

        method_to_scores_flatref = {}
        method_to_scores_avgposref = {}
        method_to_scores_shuffref = {}
        method_to_ism_score = {}

        scores_file_name = options.dir+"/imp_scores_"+model_id+".h5"
        print("Saving scores to",scores_file_name)
        #!rm $scores_file_name
        file_to_save_in = h5py.File(scores_file_name)
        file_to_save_in.create_dataset("onehot",data=subset_onehot)

        for method_name in [
                            'grad_times_inp',
                            'integrated_grad2',
                            'integrated_grad5',
                            'integrated_grad10',
                            'integrated_grad20',
                            'deeplift_rescale',
                            'deeplift_genomicsdefault'
                           ]:
            print(method_name)
            print("flatref")
            scoring_func = method_name_to_scoring_func[method_name]
            start = time.time()
            scores_flatref = np.array(
             scoring_func(input_data_list=[subset_onehot],
             input_references_list=[np.zeros_like(subset_onehot)],
             task_idx=0, batch_size=10, progress_update=1000))
            print("Time taken for",method_name,"flatref",time.time()-start)
            file_to_save_in.create_dataset("scores_"+method_name+"_flatref",
                                           data=np.sum(scores_flatref,axis=-1))
            print("avgposref")
            start = time.time()
            scores_avgposref = np.array(
                scoring_func(
                 input_data_list=[subset_onehot],
                 input_references_list=[
                  np.array([avg_gcref[0] for x in subset_onehot])],
                 task_idx=0, batch_size=10, progress_update=1000))
            print("Time taken for",method_name,"avgposref",time.time()-start)
            file_to_save_in.create_dataset(
                "scores_"+method_name+"_avgposref",
                data=np.sum(scores_avgposref,axis=-1))
            method_to_scores_flatref[method_name] = scores_flatref
            method_to_scores_avgposref[method_name] = scores_avgposref

        for method_name in ['deeplift_rescale_dinucshuff',
                            'deeplift_genomicsdefault_dinucshuff',
                            'integrated_grad2_dinucshuff',
                            'integrated_grad5_dinucshuff',
                            'integrated_grad10_dinucshuff',
                            'integrated_grad20_dinucshuff']:
            print(method_name)
            start = time.time()
            scores_shuffref = method_name_to_scoring_func[method_name](
                task_idx=0,
                input_data_sequences=subset_seqs,
                num_refs_per_seq=10,
                batch_size=200, seed=1,
                progress_update=1000)
            print("Time taken for",method_name,time.time()-start)
            file_to_save_in.create_dataset(
             "scores_"+method_name,data=np.sum(scores_shuffref,axis=-1))
            method_to_scores_shuffref[method_name] = scores_shuffref

        for method_name in ['ism']:
            print(method_name)
            start = time.time()
            scoring_func = method_name_to_scoring_func[method_name]
            scores_ism = np.array(
             scoring_func(input_data_list=[subset_onehot],
                          progress_update=10000))
            print("Time taken for",method_name,time.time()-start)
            file_to_save_in.create_dataset(
             "scores_"+method_name,data=np.sum(scores_ism,axis=-1))
            method_to_ism_score[method_name] = scores_ism

        file_to_save_in.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_ids", nargs="+", required=True)
    parser.add_argument("--subsample_rate", type=int, default=10)
    parser.add_argument("--dir", required=True)
    options = parser.parse_args()
    compute_imp_scores(options)
