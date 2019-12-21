import run_squad_v2_3

args = """--model_type albert 
    --model_name_or_path albert-xxlarge-v2
    --do_train 
    --do_eval
    --version_2_with_negative
    --train_file train-v2.0.json
    --predict_file dev-v2.0.json
    --learning_rate 3e-5 
    --num_train_epochs 2 
    --max_seq_length 384 
    --doc_stride 128 
    --output_dir albert_en
    --per_gpu_eval_batch_size=3   
    --per_gpu_train_batch_size=3  
    --overwrite_cache 
    --save_steps=1000000000 
    """.split() # --eval_all_checkpoints

import os
import __main__ as main
print("Script: " + os.path.basename(main.__file__))
print(args)

results = run_squad_v2_3.main(args=args)
import json
import datetime
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")

outname = "results " + os.path.basename(main.__file__)[:-3] + " " + date
with open(outname + ".json", "w") as out:
   json.dump(results, out)

print(args)
print("Script: " + os.path.basename(main.__file__))