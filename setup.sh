# Create a virtual environment for your project
if [ ! -d "env" ];
then
    echo "Creating virtual environment for your project"
    python3 -m venv env
    source env/bin/activate
fi

# Install requirements
echo "Installing requirements"
pip3 install -r requirements.txt

# Bake DB
echo "Baking the DB for your local setup"
python3 manage.py migrate

# Create superuser
echo "Do you want to create superuser? (y/n)"
read isSuperUserToBeCreated
if [ $isSuperUserToBeCreated = "y" ];
then
    python3 manage.py createsuperuser
fi

# Cleaning existing data
echo "Do you want to clear existing data? It'll anyway download all the data (y/n)"
read clearData
if [ $clearData = "y" ];
then
    python3 manage.py clear_data
fi

# Add data
echo "\n\nAdding Data\n"
python3 manage.py add_data
