from huggingface_hub import HfFileSystem
import pyarrow.dataset as ds

# 1. Initialize the file system with STRICT network rules
# Setting cache_type to 'none' and shrinking the block size prevents 
# the reader from accidentally buffering adjacent image bytes.
fs = HfFileSystem(default_cache_type="none", default_block_size=1024)

# 2. Locate the Parquet files for the specific split
parquet_files = fs.glob("datasets/SingleBicycle/4KLSDB/data/*train_x16*.parquet")

all_urls = set()

print(f"Found {len(parquet_files)} Parquet files")

# 3. Mount the remote files as a PyArrow dataset
arrow_dataset = ds.dataset(parquet_files, filesystem=fs, format="parquet")

# 4. Stream only the URL column in chunks
for batch in arrow_dataset.scanner(columns=["url"]).to_batches():

  # Convert the PyArrow array to a standard Python list
  urls = batch["url"].to_pylist()
  print("urls fetched:", len(urls))

  # Write out the URLs
  for url in urls:
    all_urls.add(url)
  print("all urls:", len(all_urls))
    
print("writing urls...")
with open("4KLSDB_urls.txt", "w") as f:
  for url in all_urls:
    f.write(url+"\n")
            
print("Extraction complete!")
