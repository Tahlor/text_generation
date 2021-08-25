#from transformers import datasets
#from datasets import list_datasets
import datasets

#train_ds, test_ds = datasets.load_dataset('bookcorpus', split=['train', 'test'])
train_ds = datasets.load_dataset('bookcorpus', split=['train'])
