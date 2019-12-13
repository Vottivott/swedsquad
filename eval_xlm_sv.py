import run_squad_fixed

args = """--model_type xlm 
    --model_name_or_path xlm-mlm-17-1280
    --do_eval 
    --train_file  squad_train.json
    --predict_file confident_translated_dev_no_impossible.json
    --learning_rate 3e-5 
    --num_train_epochs 2 
    --max_seq_length 384 
    --doc_stride 128 
    --output_dir xlm
    --per_gpu_eval_batch_size=3   
    --per_gpu_train_batch_size=3   
    --save_steps=2000 
    """.split() # --eval_all_checkpoints

print(args)

results = run_squad_fixed.main(args)
import json
import datetime
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")
outname = "results " + " " + date
with open(outname + ".json", "w") as out:
   json.dump(results, out)

print(args)