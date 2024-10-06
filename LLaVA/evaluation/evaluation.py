import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from pycocoevalcap.cider.cider import Cider
from nltk.translate.meteor_score import meteor_score
from bert_score import score as bert_score
import nltk
import json
import os
from PIL import Image

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

def load_data(file_path):
    return pd.read_csv(file_path)

def evaluate_bleu(predictions, references):
    smoothie = SmoothingFunction().method4
    bleu_scores = []
    for pred, ref in zip(predictions, references):
        score = sentence_bleu([ref.split()], pred.split(), smoothing_function=smoothie)
        bleu_scores.append(score)
    return bleu_scores

def evaluate_rouge(predictions, references):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = []
    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        rouge_scores.append(scores)
    return rouge_scores

def evaluate_cider(predictions, references):
    cider_scorer = Cider()
    hypo = {i: [pred] for i, pred in enumerate(predictions)}
    ref = {i: [ref] for i, ref in enumerate(references)}
    (score, _) = cider_scorer.compute_score(ref, hypo)
    return score

def evaluate_meteor(predictions, references):
    meteor_scores = []
    for pred, ref in zip(predictions, references):
        score = meteor_score([ref.split()], pred.split())
        meteor_scores.append(score)
    return meteor_scores

def evaluate_bertscore(predictions, references):
    P, R, F1 = bert_score(predictions, references, lang="en", rescale_with_baseline=True)
    avg_f1 = sum(F1) / len(F1)
    return avg_f1.item()

def main(data_file):
    data = load_data(data_file)
    
    # Extract columns
    images = data['image_path'].tolist()
    predictions = data['predicted_caption'].tolist()
    references = data['ground_truth_caption'].tolist()

    # Evaluate BLEU
    bleu_scores = evaluate_bleu(predictions, references)
    avg_bleu = sum(bleu_scores) / len(bleu_scores)
    print(f'Average BLEU Score: {avg_bleu}')
    
    # Evaluate ROUGE
    rouge_scores = evaluate_rouge(predictions, references)
    avg_rouge1 = sum([score['rouge1'].fmeasure for score in rouge_scores]) / len(rouge_scores)
    avg_rouge2 = sum([score['rouge2'].fmeasure for score in rouge_scores]) / len(rouge_scores)
    avg_rougeL = sum([score['rougeL'].fmeasure for score in rouge_scores]) / len(rouge_scores)
    print(f'Average ROUGE-1 F1 Score: {avg_rouge1}')
    print(f'Average ROUGE-2 F1 Score: {avg_rouge2}')
    print(f'Average ROUGE-L F1 Score: {avg_rougeL}')
    
    # Evaluate CIDEr
    avg_cider = evaluate_cider(predictions, references)
    print(f'Average CIDEr Score: {avg_cider}')
    
    # Evaluate METEOR
    meteor_scores = evaluate_meteor(predictions, references)
    avg_meteor = sum(meteor_scores) / len(meteor_scores)
    print(f'Average METEOR Score: {avg_meteor}')
    
    # Evaluate BERTScore
    avg_bertscore = evaluate_bertscore(predictions, references)
    print(f'Average BERTScore: {avg_bertscore}')

    # Save evaluation results
    results = {
        "BLEU": avg_bleu,
        "ROUGE-1": avg_rouge1,
        "ROUGE-2": avg_rouge2,
        "ROUGE-L": avg_rougeL,
        "CIDEr": avg_cider,
        "METEOR": avg_meteor,
        "BERTScore": avg_bertscore,
        "Notes": {
            "BLEU": "Range: 0 to 1. Higher is better. Measures the precision of n-grams in the predicted text.",
            "ROUGE-1": "Range: 0 to 1. Higher is better. Measures the overlap of unigrams (single words) between the predicted and reference texts.",
            "ROUGE-2": "Range: 0 to 1. Higher is better. Measures the overlap of bigrams (two-word sequences) between the predicted and reference texts.",
            "ROUGE-L": "Range: 0 to 1. Higher is better. Measures the longest common subsequence (LCS) between the predicted and reference texts.",
            "CIDEr": "Range: 0 to infinity. Higher is better. Measures the similarity of the predicted text to multiple reference texts using TF-IDF weighting.",
            "METEOR": "Range: 0 to 1. Higher is better. Considers synonyms, stemming, and exact matches to evaluate the quality of the predicted text.",
            "BERTScore": "Range: 0 to 1. Higher is better. Uses BERT embeddings to measure the semantic similarity between the predicted and reference texts."
        }
    }
    
    with open('evaluation_results_ours.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("Evaluation results saved to 'evaluation_results_ours.json'.")

if __name__ == "__main__":
    main('/media/akoubaa/new_ssd/naseif/Desktop/capstone/evaluation/data_llava_ours.csv')
