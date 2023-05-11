import psutil
import os
import easygui as eg

def show_processes():
    output = os.popen("ps aux").read()
    process_amount = os.popen("ps ax | grep -v 'ps aux\|grep' | wc -l").read()
    processes = output.split('\n')[1:]  # skip first line
    options = []
    for process in processes:
        if process != '':
            process_data = process.split()
            pid = process_data[1]
            name = ''
            try:
                name = psutil.Process(int(pid)).name()
            except psutil.NoSuchProcess:
                name = 'Unknown'
            cmd = ' '.join(process_data[10:])
            options.append(pid + ' ' + name + ' ' + cmd)
    choice = eg.choicebox("Showing all running processes:\n\n\nTotal amount of running processes: "+str(process_amount)+"\n\n\nTo filter and view a specific process, double click on it, or select it and click Ok", choices=options)
    if choice is None:
        return
    for i in options:
        if i in choice:
            output = os.popen("ps aux | grep -v 'ps aux\|grep' "+i).read()
            eg.msgbox("Showing selected process in detailed view: \n\n"+str("PID: "+i+"\n\n")+"\n", title="Process view")
            break
    #return
    pid = choice.split()[0]

def kill_process():
    grep = eg.enterbox("In the following prompt, type one of the following data requested:\n\n  - Application or process name\n  - PID number\n  - Command instance\n  - String to find in running processes list.\n\n\nNOTE: To simply view a full list of the processes, just press enter", title="Processes finder prompt")
    if grep is None:
        return
    output = os.popen("ps aux").read()
    processes = output.split('\n')[1:]  # skip first line
    process_amount = os.popen("ps ax | grep -v 'ps aux\|grep' | wc -l").read()
    options = []
    for process in processes:
        if process != '':
            process_data = process.split()
            pid = process_data[1]
            name = ''
            try:
                name = psutil.Process(int(pid)).name()
            except psutil.NoSuchProcess:
                name = 'Unknown'
            cmd = ' '.join(process_data[10:])
            if grep in cmd or grep in name or grep == pid:
                options.append(pid + ' ' + name + ' ' + cmd)
    if not options:
        error_image = "/home/gus/Desktop/myfiles/Tecnologia/Programming/Python_programs/Linux_Processes/redcross.png"
        eg.msgbox("No valid data was provided. A process couldn´t be found\n\n\n                Press ok to get back to the main menu", "Error - No data provided", image=error_image)
        return
    choice = eg.choicebox("Total amount of processes running: "+str(process_amount)+"\n\nChoose a process from the list.\n\nTo Kill the process, double clicked on it, or select it and click Ok.\n\nATTENTION: You will be warned, and have to confirm the killing of the process, in another window instance:", title="Running processes window", choices=options)
    if choice is None:
        return
    pid = choice.split()[0]
    warning_image="/home/gus/Desktop/myfiles/Tecnologia/Programming/Python_programs/Linux_Processes/warning.png"
    choices=["Yes", "No"]
    choice = eg.buttonbox("WARNING!: You have requested to terminate process: "+str(pid)+".\n\n\n                  Do you confirm the termination of this process?", title="Confirm process kill", choices=choices, image=warning_image)
    if choice == "Yes":
        kill_process_img="/home/gus/Desktop/myfiles/Tecnologia/Programming/Python_programs/Linux_Processes/process_kill.png"
        os.popen("sudo kill -9 " + pid)
        eg.msgbox("Process with PID " + pid + " has been killed.\n\nPress Ok to get back to the processes screen", "Success", image=kill_process_img)
    if choice == "No":
        abort_image="/home/gus/Desktop/myfiles/Tecnologia/Programming/Python_programs/Linux_Processes/abort.png"
        eg.msgbox("You decided to abort the termination of PID: "+str(pid)+"\n\n", title="Aborted Kill process", image=abort_image)


while True:
    main_image="/home/gus/Desktop/myfiles/Tecnologia/Programming/Python_programs/Linux_Processes/linux_processes.png"
    choice = eg.buttonbox("\n\nThis program finds a process based on an input provided by the user\n\nand attempts to terminate it.\n\n\nWARNING: This program requires the user to be a sudoer. Use with caution.\n\n\nPress a button below to start operating:", title="Linux Process Gui", image=main_image, choices=["Find a process to terminate", "Show all processes"])
    if choice == "Find a process to terminate":
        kill_process()
    if choice == "Show all processes":
        show_processes()
    if choice == None:
        break

