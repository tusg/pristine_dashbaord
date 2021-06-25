from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import webbrowser


app = Flask(__name__,template_folder='template')


@app.route('/stop')
def kill_all(proc):
    #time.sleep(10)
    #pid = int(str(res).split(" ")[3])
    process = subprocess.Popen("ps aux | grep {val}| awk '{{print$2}}'".format(val = proc), shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res,err = process.communicate()
    pid_lst = res.decode("utf-8").split('\n')
    print(pid_lst)
    for pid in pid_lst:
        if len(pid) > 1:
            try:
                process = subprocess.Popen("kill {val}".format(val = int(pid)), shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                #os.kill(int(pid),signal.SIGTERM)
                print("killing the process....{pid}".format(pid=pid))
            except:
                print("unable to kill the pid-- {pid}".format(pid=pid))
                continue
        else:
            print("process not running for pid - {pid}".format(pid = pid))
    print("stopped all the processes")
    return


@app.route('/start')
def run_in_terminal(command):
    print(command)
    subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return



@app.route('/tables')
def show_tables():
    df = pd.read_csv(os.path.join(os.getcwd(),'template/prsitine_dashboard.csv'))
    urls = df[df['Environment'].str.contains('http') == True]
    urls.columns=['Application Names','Urls']
    urls['Urls'] = urls['Urls'].apply(lambda x: '<a href="{0}" target="_blank">link</a>'.format(x))
    urls['Urls'] = urls.apply(lambda x: x['Urls'].replace('link',x['Application Names']), axis=1)
    services = df.drop(urls.index)
    services.columns=['Application Names','Services']
    #services['Services'] = services['Services'].apply(lambda x: '<a href="{0}">Start</a> <a href="{0}"> Stop</a>'.format(x))
    #services['Services'] = services.apply(lambda x: x['Services'].replace('Start','Start ' + x['Application Names'].split("_")[0]), axis=1)
    #services['Services'] = services.apply(lambda x: x['Services'].replace('Stop','Stop ' + x['Application Names'].split("_")[0]), axis=1)
    return urls

@app.route('template/pristine_dashboard.html', methods=("POST", "GET"))
def html_table():
    urls = show_tables()
    return render_template('template/pristine_dashboard.html',  tables=[urls.to_html(escape=False,index=False)])

if __name__ == '__main__':
    #webbrowser.open_new('http://127.0.0.1:2000/')
    app.run()
