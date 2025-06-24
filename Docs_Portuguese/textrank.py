import os import glob import spacy import pke

# --- STEP 1: Load Portuguese stopwords --- print("🔹 Loading Portuguese stopwords...") nlp = spacy.load("pt_core_news_sm") stopwords = set(nlp.Defaults.stop_words) print(f"✅ Loaded {len(stopwords)} stopwords.\n")

def remove_stopwords_pt(text):     doc = nlp(text)     return " ".join(token.text for token in doc if token.text.lower() not in stopwords)

# --- STEP 2: Define TextRank model --- model_name = "TextRank" model_class = pke.unsupervised.TextRank print(f"🔹 Model selected: {model_name}\n")

# --- STEP 3: Define input & output paths --- input_folder = "/Users/elmirasalari/Pesticides/Portugues-txt-2"  # adjust if needed

output_folder_without_filtering = os.path.join("/Users/elmirasalari/Pesticides/Results", f"{model_name}_without_Filtering") output_folder_after_filtering = os.path.join("/Users/elmirasalari/Pesticides/Results", f"{model_name}_After_Filtering")

# Ensure output folders exist os.makedirs(output_folder_without_filtering, exist_ok=True) os.makedirs(output_folder_after_filtering, exist_ok=True)

# --- STEP 4: Process all .txt files --- txt_files = glob.glob(os.path.join(input_folder, "*.txt")) print(f"📂 Found {len(txt_files)} text files.\n")

for file_path in txt_files:     print(f"📄 Processing file: {file_path}")

# A) Read file content     with open(file_path, "r", encoding="utf-8") as f:         text = f.read()     print("   ✅ File read.")

# B) Remove stopwords before extraction     clean_text = remove_stopwords_pt(text)     print("   ✅ Stopwords removed.")

# C) Initialize extractor (TextRank)     extractor = model_class()

# D) Load cleaned text     extractor.load_document(input=clean_text, language='pt')     print("   ✅ Document loaded.")

# E) Candidate selection (no arguments)     extractor.candidate_selection()     print("   ✅ Candidate selection done.")

# F) Candidate weighting     extractor.candidate_weighting()     print("   ✅ Candidate weighting completed.")

# G) Get top 50 keyphrases without filtering     keyphrases = extractor.get_n_best(n=50)     print(f"   🔹 Extracted {len(keyphrases)} keyphrases (without filtering).")

# Save without filtering     base_name = os.path.splitext(os.path.basename(file_path))[0]     output_file_no_filter = os.path.join(output_folder_without_filtering, f"{base_name}_keywords.txt")

with open(output_file_no_filter, "w", encoding="utf-8") as out_f:         for phrase, _score in keyphrases:             out_f.write(phrase + "\n")     print(f"✅ Saved keywords without filtering to: {output_file_no_filter}")

# H) Filter to 1-2 word phrases only     filtered_keyphrases = [phrase for phrase, _score in keyphrases if len(phrase.split()) <= 2]     print(f"   🔹 Filtered down to {len(filtered_keyphrases)} keyphrases (1-2 words only).")

# Save after filtering     output_file_filtered = os.path.join(output_folder_after_filtering, f"{base_name}_keywords.txt")

with open(output_file_filtered, "w", encoding="utf-8") as out_f:         for phrase in filtered_keyphrases:             out_f.write(phrase + "\n")     print(f"✅ Saved filtered keywords to: {output_file_filtered}\n")

