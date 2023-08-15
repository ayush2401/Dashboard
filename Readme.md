# Install virtual env

pip install virtualenv

# make new env

python -m virtualenv env

# activate

cd env
cd Scripts
.\activate
cd ..

# clone the repo

cd dashboard

python manage.py runserver