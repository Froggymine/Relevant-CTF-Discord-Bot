if [ -s secret.txt ]; then
        # The file is not-empty.
        main-venv/bin/python3 main.py
else
        # The file is empty.
        echo "Please add discord developer bot secret token to secret.txt"
fi