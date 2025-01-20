import yaml, json, os, shutil, subprocess
from datetime import datetime, timezone, timedelta

#ENV Variable
WORKDIR = '/workspaces'
ZMK_CONFG_PATH = '/workspaces/zmk-config'


def run_shell_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

def mkdir(dir):
    if not os.path.exists(dir): 
        os.makedirs(dir)

def rm(dir):
    if os.path.exists(dir): 
        shutil.rmtree(dir)   

def zmk_build(board, shield, zmkConfigPath=None, releaseDir=None):
    print(board)
    print(shield)
    
    #set variable
    destDir = WORKDIR + '/build/' + board  + '/' + shield

    if releaseDir==None:
        releaseDir = ZMK_CONFG_PATH + '/release' 
    else:
        releaseDir = ZMK_CONFG_PATH + '/release/'  + releaseDir

    if zmkConfigPath==None:
        zmkConfigCommand = ""
    else:
        zmkConfigCommand = '-DZMK_CONFIG=' + zmkConfigPath
    #command = 'west build  -d "' + destDir + '" -s zmk/app -b "' + board + '" -- ' + zmkConfigCommand + ' -DSHIELD="' + shield + '"' 
    command = 'west build  -d "' + destDir + '" -s zmk/app -b "' + board + '" -S studio-rpc-usb-uart -- ' + zmkConfigCommand + ' -DSHIELD="' + shield + '"' 
                            
    print(destDir)
    print(releaseDir)
    print(command)


    #prepare dir
    mkdir(destDir)
    mkdir(releaseDir)

    #build
    run_shell_command(command)   

    #copy release dir
    shutil.copy(destDir + '/zephyr/zmk.uf2', releaseDir + '/' + shield + '_' + board + '.uf2')

def main():
    #change current dir
    os.chdir(WORKDIR)
    print(os.getcwd())

    timedelta
    tz_offset = os.popen('date +%z').read().strip() 
    hours_offset = int(tz_offset[:3]) 
    minutes_offset = int(tz_offset[0] + tz_offset[3:]) 
    local_tz = timezone(timedelta(hours=hours_offset, minutes=minutes_offset)) 
    now_local = datetime.now(local_tz)
    timestamp = now_local.strftime('%Y%m%d%H%M%S')

    #west update
    mkdir('/workspaces/app/')
    shutil.copy(ZMK_CONFG_PATH + '/config/west.yml', '/workspaces/app/')
    run_shell_command('west update')   
    run_shell_command('west zephyr-export')   

    #clear & backup release dir
    #src_dir = ZMK_CONFG_PATH + '/release'
    #dst_dir = ZMK_CONFG_PATH + '/release/backup' 
    #if os.path.exists(src_dir): 
    #    for p in os.listdir(src_dir):
    #        rm(os.path.join(dst_dir, p))
    #        shutil.move(os.path.join(src_dir, p), dst_dir)

    #build keyboard by build.yaml
    with open(ZMK_CONFG_PATH + '/build.yaml') as file:
        obj = yaml.safe_load(file)
        #js = json.dumps(obj, indent=2)
        
        for shield in obj["include"]:
            print(shield)
            zmk_build(shield["board"], shield["shield"],  ZMK_CONFG_PATH + '/config', timestamp)

if __name__ == '__main__':
    main()
