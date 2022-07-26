from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(np.round(popular_df['num_ratings'].values,2)),
                           rating=list(np.round(popular_df['avg_rating'].values,2))
                           )


@app.route('/recommend')
def recommend_ui():
    book_list=list(pt.reset_index().drop_duplicates('Book-Title')['Book-Title'].values)
    return render_template('recommend.html',book_list=book_list)


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input =request.form.get('Tag')
    if user_input:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                data.append(item)
            book_list=list(pt.reset_index().drop_duplicates('Book-Title')['Book-Title'].values)
            return render_template('recommend.html',data=data,book_list=book_list)
  
       

if __name__ == '__main__':
    app.run(debug=True)