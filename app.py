from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://yello3617:yello_3617@cluster0.u44ezk2.mongodb.net/")
db = client.memo_db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['POST'])
def save_memo():
    data = request.get_json()
    title = data['title']
    content = data['content']
    doc = {'title': title, 'content': content, 'likes': 0}
    db.memos.insert_one(doc)
    return jsonify({'msg': '저장 완료'})

@app.route('/memo', methods=['GET'])
def get_memos():
    memos = list(db.memos.find({}).sort('likes', -1))
    for memo in memos:
        memo['_id'] = str(memo['_id'])
    return jsonify({'memos': memos})

@app.route('/memo/<id>', methods=['DELETE'])
def delete_memo(id):
    db.memos.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': '삭제 완료'})

@app.route('/memo/<id>', methods=['PUT'])
def update_memo(id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    db.memos.update_one({'_id': ObjectId(id)}, {'$set': {'title': title, 'content': content}})
    return jsonify({'msg': '수정 완료'})

@app.route('/memo/like/<id>', methods=['POST'])
def like_memo(id):
    db.memos.update_one({'_id': ObjectId(id)}, {'$inc': {'likes': 1}})
    return jsonify({'msg': '좋아요 반영됨'})

if __name__ == '__main__':
    app.run(debug=True)
