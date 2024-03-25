# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан
# cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с
# данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты.

from flask import Flask, render_template, make_response, request, redirect

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    name = request.form['name']
    email = request.form['email']
    # устанавливаем cookie
    response = make_response(redirect('/hello'))
    response.set_cookie('name', name)
    response.set_cookie('email', email)

    return response


@app.route('/hello')
def hello():
    name = request.cookies.get('name')
    return render_template('hello.html', name=name)


@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('name')
    response.delete_cookie('email')

    return response



if __name__ == '__main__':
    app.run(debug=True)
