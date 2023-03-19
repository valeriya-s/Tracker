using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class SocketClient : MonoBehaviour
{

    // Use this for initialization

/*    public GameObject hero;*//*
    private float xPos = 10.0f;
    private Vector3 legPos;*/

    public GameObject[] Right = new GameObject[6];
    public GameObject[] Left = new GameObject[6];

    // private float xPos = 10.0f;

    public float[] xList = new float[12];
    public float[] yList = new float[12];
    public float[] zList = new float[12];

    public int index1 = 0;

    Thread receiveThread;
    UdpClient client;
    public int port;

    public int partNum = 0;

    //info

    public string lastReceivedUDPPacket = "";
    public string allReceivedUDPPackets = "";

    void Start()
    {
        init();
    }

    void OnGUI()
    {
        Rect rectObj = new Rect(40, 10, 200, 400);

        GUIStyle style = new GUIStyle();

        style.alignment = TextAnchor.UpperLeft;

        GUI.Box(rectObj, "# UDPReceive\n127.0.0.1 " + port + " #\n"

                  //+ "shell> nc -u 127.0.0.1 : "+port +" \n"

                  + "\nLast Packet: \n" + lastReceivedUDPPacket

                  //+ "\n\nAll Messages: \n"+allReceivedUDPPackets

                  , style);

    }

    private void init()
    {
        print("UPDSend.init()");

        port = 5065;

        print("Sending to 127.0.0.1 : " + port);

        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
/*        legPos = hero.transform.position; 
*/
    }

    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);
                print(">> " + text);
                lastReceivedUDPPacket = text;
                allReceivedUDPPackets = allReceivedUDPPackets + text;
                /*xPos = float.Parse(text);
                xPos *= 1.0f;*/

                if (partNum == 0)
                {
                    xList[index1] = float.Parse(text);
                }

                if (partNum == 1)
                {
                    yList[index1] = float.Parse(text);
                }

                if (partNum == 2)
                {
                    zList[index1] = float.Parse(text);
                    if (index1 == 21)
                    {
                        index1 = 0;
                    }
                    else
                    {
                        index1 = index1 + 1;
                    }
                }

                // Cycle through the 3 data points
                partNum = partNum + 1;
                if (partNum == 3)
                {
                    partNum = 0;
                }
            }
            catch (Exception e)
            {
                print(e.ToString());
            }
        }
    }

    public string getLatestUDPPacket()
    {
        allReceivedUDPPackets = "";
        return lastReceivedUDPPacket;
    }

    // Update is called once per frame
    void Update()
    {
        /*        hero.transform.position = new Vector3(legPos.x + (xPos*2.0f), legPos.y, legPos.z);
        */
        // hero.transform.position = new Vector3(xPos - 6.0f, -3, 0);
        int ind2 = 0;

        for (int jj = 0; jj < 6; jj++)
        {

            Right[jj].transform.position = new Vector3(3.264f * xList[ind2], 1.836f * yList[ind2], 0); // zList[ind2]);
            Left[jj].transform.position = new Vector3(3.264f * xList[ind2 + 1], 1.836f * yList[ind2 + 1], 0); // zList[ind2+1]);

            ind2 = ind2 + 2;
        }
    }

    void OnApplicationQuit()
    {
        if (receiveThread != null)
        {
            receiveThread.Abort();
            Debug.Log(receiveThread.IsAlive); //must be false
        }
    }
}