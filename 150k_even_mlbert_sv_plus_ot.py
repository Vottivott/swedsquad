import run_squad

args = """--model_type bert 
    --model_name_or_path bert-base-multilingual-cased
    --eval_all_checkpoints 
    --do_eval 
    --train_file confident_plus_ot_train_no_impossible.json
    --predict_file squad_dev.json
    --learning_rate 3e-5 
    --max_steps 150000 
    --max_seq_length 384 
    --doc_stride 128 
    --output_dir 150k_mlbert_sv_plus_ot
    --per_gpu_eval_batch_size=3   
    --per_gpu_train_batch_size=3 
    --overwrite_cache  
    --save_steps=2000 
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