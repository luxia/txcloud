from flask import Flask,render_template,request
import requests
import re
import os
######
######

def geturl(url):
	##获得cookie
    打开腾讯cookie = open('cookies.txt', 'r')
    腾讯cookie = 打开腾讯cookie.read()
    打开腾讯cookie.close()
    cookies = {
        'Cookie': 腾讯cookie
    }
    ##获得vid
    腾讯视频页面url = requests.get(url=url, cookies=cookies)
    视频页面源码 = 腾讯视频页面url.text
    提取vid的规则 = r'&vid=(.*?)&ptag='
    提取的vid = re.findall(提取vid的规则, str(视频页面源码))
    vid = 提取的vid[0]
    ##mp4
    mp4url = url = 'http://h5vv.video.qq.com/getinfo?vid={}'.format(vid)
    打开mp4页面 = requests.get(url=mp4url, cookies=cookies)
    mp4页面 = 打开mp4页面.text
    ##m3u8
    接口url = 'http://h5vv.video.qq.com/getinfo?defn=fhd&platform=10801&type=json&sdtfrom=v1000&appVer=1&vid={}&newnettype=1&fhdswitch=1&show1080p=1&dtype=3'.format( vid)
    接口页面 = requests.get(url=接口url, cookies=cookies)  # 没有cookie，就5分钟
    接口页面源码 = 接口页面.text
    提取播放链接规则1 = r'</type><ul><ui><url>(.*?)</url><vt>'
    提取播放链接规则2 = r'</hls></ui><ui><url>(.*?)</url><vt>'
    提取播放链接规则2 = r'</hls></ui><ui><url>(.*?)</url><vt>'
    提取播放名称规则 = r'<pt>(.*?)</pt></hls>'
    提取的链接1 = re.findall(提取播放链接规则1, str(接口页面源码))
    提取的链接2 = re.findall(提取播放链接规则2, str(接口页面源码))
    提取的名称 = re.findall(提取播放名称规则, str(接口页面源码))
    链接1 = 提取的链接1[0]
    链接2 = 提取的链接2[0]
    链接3 = 提取的链接2[1]
    名称 = 提取的名称[0]
    判断链接 = re.search(r'http://lts', 链接1, re.M | re.I)  # 1有就返回1，
    判断链接2 = re.search(r'http://lts', 链接2, re.M | re.I)  # 2有就返回2
    判断链接3 = re.search(r'http://lts', 链接3, re.M | re.I)  # 3有就返回3，
    # 3个链接只返回一个带http:ip/的链接，那个才是真的
    if (判断链接 == None):
	    return 链接1 + 名称
    elif (判断链接2 == None):
        return 链接2 + 名称
    else:
        return 链接3 + 名称


app = Flask(__name__)

@app.route('/')
def index():###主页面
    return render_template('/index.html')


@app.route('/api', methods=['post', 'get'])
def api():####api
    url = request.args.get('url')
    paly_url2 = geturl(url)
    return render_template('/play.html', playurl = paly_url2)

@app.route('/admin')
def admin():
    return render_template('/login.html')

@app.route('/admin/api', methods=['POST'],strict_slashes=False)
def admin_api():
    fname =  request.form['fname']
    if (fname == "admin"):####后台认证密码
        return render_template('/admin.html')
    else:
        return "密码错误，请重新输入"

@app.route('/api/start', methods=['POST'], strict_slashes=False)
def api_name():
    pd = request.form['password']
    file = open('/cookies.txt','w',encoding='utf-8')
    file.write(pd)
    file.close()
    return "更新cookie成功"



@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
