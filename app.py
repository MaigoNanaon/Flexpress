from flask import Flask, render_template, request
import os
import csv
import json
import random
import utili

app = Flask(__name__)



def generate_data(mode):
    folder_data = []
    questions = []
    n = 7
    if mode == 'smos':
        gen_dir = os.listdir('./static/smos/gen')
        ori_dir = os.path.join('./static/ESD')
        sams = random.sample(gen_dir, n)
        for i in range(len(sams)):
            
            filename = os.path.basename(sams[i])
            emo = utili.decide_emo(filename)[1]
            spk = filename[:4]
            ref_sam = random.sample(os.listdir(os.path.join(ori_dir, spk)), 1)[0]
            ref_audio = os.path.join(ori_dir+'/'+spk+"/"+ref_sam)
            test_audio = os.path.join('./static/smos/gen/'+filename)
            print(ref_audio, test_audio)
            questions.append({
                'question_id': i,
                'emo':emo,
                'ref_audio': ref_audio,
                'test_audio': test_audio,
            })
            
    return questions




@app.route('/smos')
def index():
    questions = generate_data(mode='smos')
    return render_template('emos.html', questions=questions)


@app.route('/smos/submit', methods=['POST'])
def submit():
    username = request.form.get('username')  # 获取用户的用户名
    if not username:
        return "用户名不能为空，请返回并输入用户名！"
    csv_file = username + "_" + 'smos.csv'
    
    responses = []
    for i in range(0, 100):
        response1 = request.form.get(f'choice_{i}')
        response2 = request.form.get(f'choice2_{i}')
        response3 = request.form.get(f'choice3_{i}')
        if response1 and response2 and response3:  # 确保用户选择了一个答案
            print(response1, response2, response3)
            responses.append({'username': username, 'question_id': i,
                              'answer1': response1, 'answer2': response2, 'answer3': response3})
    
    # 将用户的答案写入CSV文件
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        for response in responses:
            writer.writerow([response['username'], response['question_id'],
                             response['answer1'], response['answer2'], response['answer3']])
    
    return "提交成功！谢谢您的参与。"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8500, debug=True)
