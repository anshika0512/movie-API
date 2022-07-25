#!/usr/bin/env python
# coding: utf-8

# # REST API IN FLASK

# In[ ]:


#install flask 
get_ipython().system('pip install flask')
get_ipython().system('pip install Flask-Cors')


# In[2]:


import import_ipynb


# In[3]:


#importing libraries
from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation


# In[5]:


#flask code
app = Flask(__name__)
CORS(app) 
        
@app.route('/movie', methods=['GET'])
def recommend_movies():
    res = recommendation.results(request.args.get('title'))
    return jsonify(res)

if __name__=='__main__':
    app.run(port = 5000)


# In[ ]:




