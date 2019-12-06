import run_squad

args = """--model_type bert 
    --model_name_or_path bert-base-multilingual-cased
    --do_train 
    --do_eval 
    --train_file  squad_train.json
    --predict_file squad_dev.json 
    --learning_rate 3e-5 
    --num_train_epochs 2 
    --max_seq_length 384 
    --doc_stride 128 
    --output_dir "./mlbert" 
    --per_gpu_eval_batch_size=3   
    --per_gpu_train_batch_size=3   
    --save_steps=2000 
    --eval_all_checkpoints 
    --overwrite_output_dir 
    --overwrite_cache
    """.split()

run_squad.main(args)