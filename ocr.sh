find -name "*.pdf" | xargs -i ocrmypdf {} {} -l deu --rotate-pages --title {} --clean --rotate-pages-threshold 5
