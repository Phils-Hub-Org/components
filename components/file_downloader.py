import os, requests

class FileDownloader:

    @staticmethod
    def download_file(url: str, save_path: str) -> None:
        """Downloads the file from a secured URL, ensuring the directory exists."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f'File downloaded successfully to {save_path}')
        except requests.exceptions.SSLError as ssl_err:
            print(f'SSL error occurred: {ssl_err}')
        except requests.exceptions.RequestException as req_err:
            print(f'Error during requests to {url}: {req_err}')
        except Exception as e:
            print(f'An error occurred: {e}')

# Example usage
if __name__ == '__main__':
    # Dropbox share link (make sure to change `dl=0` to `dl=1` for direct download)
    dropbox_share_link = 'https://www.dropbox.com/scl/fi/jexp0mtauduc5xbn7afmd/scenes.zip?rlkey=94fqyyeucf5bn4lm3iyf195mj&dl=1'
    
    # Save path for the downloaded file    
    save_path = os.path.join(os.getcwd(), 'Tests', 'FileDownloader', 'download', 'scenes.zip')

    # Create an instance of the downloader with the modified Dropbox link
    FileDownloader.download_file(dropbox_share_link, save_path)
    