import re,os
from time import sleep
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional , LCD_FONT

def kill_all_process(program_string):
    ps_aux_output=os.popen("ps -aux | grep {}".format(program_string)).read().split("\n")[:-1]
    for ps_line in ps_aux_output:
        ps_line = ps_line.split(" ")
        ps_user = ps_line[0]
        for i in ps_line[1:]:
            if i != "":
                ps_pid=i
                break
        ps_app = ps_line[-2]
        ps_script = ps_line[-1]
        #print("APP: {}, SCRIPT: {}, PID: {},USER: {}".format(ps_app,ps_script,ps_pid,ps_user))
        if ps_app == "python3":
            if int(ps_pid) != os.getpid():
                #print("  -->This process will be killed (PID: {}):)".format(ps_pid))
                if ps_user  == "root":
                    return_code = os.system("sudo kill -9 {}".format(ps_pid))
                else:
                    return_code = os.system("kill -9 {}".format(ps_pid))
                
                if return_code != 0:
                    #print("There was an error killing process PID: {}".format(ps_pid))
                    exit(2) 

def get_ip():
    ipv4_pattern=re.compile("^(\d{1,3}\.){3}\d{1,3}$")
    ip_info=os.popen("hostname -I").read().split(" ")
    ip=None
    
    for i in ip_info:
        if ipv4_pattern.match(i):
            ip=i
    
    return ip

if __name__ == "__main__":
    kill_all_process("get_ip")
    serial= spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascade=1, block_orientacion=0,rotate=0,blocks_arranged_in_reverse_order=False)
    
    show_message(device,"Loocking for IP...",fill="white",font=proportional(LCD_FONT),scroll_delay=0.05)
    
    while True:
        ip=get_ip()
        if ip is None:
            #print("IP not found")
            show_message(device,"IP  not found :(",fill="white",font=proportional(LCD_FONT),scroll_delay=0.05)
            sleep(1)
        else:   
            #print("IP:{}".format(ip))
            show_message(device,"IP:{}".format(ip),fill="white",font=proportional(LCD_FONT),scroll_delay=0.05)
    sleep(3) 
