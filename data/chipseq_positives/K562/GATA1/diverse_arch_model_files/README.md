Copy pasting Eva's spreadsheet (https://docs.google.com/spreadsheets/d/1qKDv0QXwscPj9S4dqdRvqsFlsXsWY14oYNaN03Y7KJg/edit?ts=5e746ec7#gid=0) here:
```
"Architecture Description (Difference
From Original)"	Training	Validation	Model Path	model_id (added by Av)
Batch normalization layer at the end	0.835	0.81	/users/eprakash/experiments/K562/GATA1/batch_norm/batch_norm_axis_-1/momma_dragonn/examples/fasta_sequential_model/ model_files	JMAzN
Remove conv layer (15 filters, length 5)	0.833	0.806	/users/eprakash/experiments/K562/GATA1/conv_layers/remove_from_beginning/momma_dragonn/examples/fasta_sequential_model/model_files	Jy29E
"Batch normalization layer at the end and
 0.2 dropout layer at the end"	0.838	0.812	/users/eprakash/experiments/K562/GATA1/dropout/dropout_0_2_batch_norm/momma_dragonn/examples/fasta_sequential_model/model_files	vv9b1
Learning rate = 0.0005	0.81	0.807	/users/eprakash/experiments/K562/GATA1/learning_rate/lr_0_0005/momma_dragonn/examples/fasta_sequential_model/model_files	bGNjI
l2 regularization with lambda 0.01	0.825	0.808	/users/eprakash/experiments/K562/GATA1/regularization/l2/momma_dragonn/examples/fasta_sequential_model/model_files	obvUz
"l2 regularization with lambda 0.01 and 
batch normalization layer at the end"	0.828	0.812	/users/eprakash/experiments/K562/GATA1/regularization/l2_batch_norm/momma_dragonn/examples/fasta_sequential_model/model_files	JVWPP
l2 regularization with lambda 0.001	0.834	0.805	/users/eprakash/experiments/K562/GATA1/regularization/l2_lambda_0_001/momma_dragonn/examples/fasta_sequential_model/model_files	w6q9F
Add 1 conv layer (15 filters, length 5)	0.818	0.814	"/users/eprakash/experiments/K562/GATA1/conv_layers/add_conv_layer/momma_dragonn/examples/fasta_sequential_model/model_files
(record_1)"	8kMTn
Add 2 conv layers (each 15 filters, length 5)	0.807	0.81	"/users/eprakash/experiments/K562/GATA1/conv_layers/add_conv_layer/momma_dragonn/examples/fasta_sequential_model/model_files
(record_2)"	6Box2
Add dense layer (output dim 1)	0.809	0.802	/users/eprakash/experiments/K562/GATA1/dense/momma_dragonn/examples/fasta_sequential_model/model_files	9JjOB
Change conv filter length to 3	0.814	0.805	"/users/eprakash/experiments/K562/GATA1/filter/momma_dragonn/examples/fasta_sequential_model/model_files
(record_2)"	EWLCA
Change conv filter length to 10	0.818	0.798	"/users/eprakash/experiments/K562/GATA1/filter/momma_dragonn/examples/fasta_sequential_model/model_files
(record_1)"	XWdII
```
