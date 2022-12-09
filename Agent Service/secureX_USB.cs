using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.IO;
using System.Threading.Tasks;
using System.Timers;
using System.Management;
using System.Security;

namespace SecureX
{
    public partial class secureX_USB : ServiceBase
    {
        
        Timer timer = new Timer();
        public secureX_USB()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            WriteToFile("SecureX Service is started at " + DateTime.Now);
            timer.Elapsed += new ElapsedEventHandler(OnElapsedTime);
            timer.Interval = 5000; //number in milisecinds  
            timer.Enabled = true;
        }

        protected override void OnStop()
        {
            WriteToFile("SecureX Service is stopped at " + DateTime.Now);
        }

        private void OnElapsedTime(object source, ElapsedEventArgs e)
        {
            string agentRunning;
            ManagementObjectSearcher searcher = new ManagementObjectSearcher("SELECT UserName FROM Win32_ComputerSystem");
            ManagementObjectCollection collection = searcher.Get();
            string username = (string)collection.Cast<ManagementBaseObject>().First()["UserName"];
            if (Process.GetProcessesByName("SecureX USB agent").Length > 0)
            {
                agentRunning = "yes";
            }
            else
            {
                agentRunning = "no";
                    
                try
                {
                    WriteToFile("Service starting..... " + DateTime.Now + " :: " + "USER : " + username + " :: AGENT STATUS : " + agentRunning);
                    Process.Start(AppDomain.CurrentDomain.BaseDirectory + "agent\\SecureX USB agent.exe");
                    //Process.Start(AppDomain.CurrentDomain.BaseDirectory + "notification\\Notification test.exe");

                }
                catch (Exception)
                {

                    throw;
                }
            }
            //WriteToFile("Service is recall at " + DateTime.Now + username + " " + agentRunning);

        }

        public void WriteToFile(string Message)
        {
            string path = AppDomain.CurrentDomain.BaseDirectory + "\\Logs";
            if (!Directory.Exists(path))
            {
                Directory.CreateDirectory(path);
            }
            string filepath = AppDomain.CurrentDomain.BaseDirectory + "\\Logs\\ServiceLog_" + DateTime.Now.Date.ToShortDateString().Replace('/', '_') + ".txt";
            if (!File.Exists(filepath))
            {
                // Create a file to write to.   
                using (StreamWriter sw = File.CreateText(filepath))
                {
                    sw.WriteLine(Message);
                }
            }
            else
            {
                using (StreamWriter sw = File.AppendText(filepath))
                {
                    sw.WriteLine(Message);
                }
            }
        }



    }
}
