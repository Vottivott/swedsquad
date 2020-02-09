import run_squad_inter as run_squad

args = """--model_type bert 
    --model_name_or_path swe-uncased_L-24_H-1024_A-16/
    --do_lower_case
    --do_eval 
    --eval_all_checkpoints 
    --train_file confident_translated_train_no_impossible.json
    --predict_file confident_translated_dev_no_impossible.json
    --learning_rate 5e-6 
    --max_steps 160000 
    --max_seq_length 384 
    --doc_stride 128 
    --output_dir 6th_svbertlarge_naive_sv
    --per_gpu_eval_batch_size=3   
    --per_gpu_train_batch_size=3 
    --overwrite_cache  
    --save_steps=2000 
    --logging_steps=2000
    """.split() # --eval_all_checkpoints

import os
import __main__ as main
print("Script: " + os.path.basename(main.__file__))
print(args)

results = run_squad.main(args)
import json
import datetime
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")

outname = "results " + os.path.basename(main.__file__)[:-3] + " " + date
with open(outname + ".json", "w") as out:
   json.dump(results, out)

print(args)
print("Script: " + os.path.basename(main.__file__))