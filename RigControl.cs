using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class RigControl : MonoBehaviour
{
    public GameObject humanoid;
    public Vector3 bodyRotation = new Vector3(0, 0, 0);

    // new shit
    public GameObject[] Right = new GameObject[6];
    public GameObject[] Left = new GameObject[6];
    public float[] Rangle = new float[6];
    public float[] Langle = new float[6];

    Thread receiveThread;
    UdpClient client;
    public int port;

    int partNum = 0;

    public string lastReceivedUDPPacket = "";
    public string allReceivedUDPPackets = "";

    /////////////////////////////////////////

    RigBone leftUpperArm;
    RigBone leftLowerArm;
    RigBone leftUpperLeg;
    RigBone leftLowerLeg;

    RigBone rightUpperArm;
    RigBone rightLowerArm;
    RigBone rightUpperLeg;
    RigBone rightLowerLeg;

    RigBone hips;


    void Start()
    {
        init();
        leftUpperArm = new RigBone(humanoid, HumanBodyBones.LeftUpperArm);
        leftLowerArm = new RigBone(humanoid, HumanBodyBones.LeftLowerArm);
        leftUpperLeg = new RigBone(humanoid, HumanBodyBones.LeftUpperLeg);
        leftLowerLeg = new RigBone(humanoid, HumanBodyBones.LeftLowerLeg);

        rightUpperArm = new RigBone(humanoid, HumanBodyBones.RightUpperArm);
        rightLowerArm = new RigBone(humanoid, HumanBodyBones.RightLowerArm);
        rightUpperLeg = new RigBone(humanoid, HumanBodyBones.RightUpperLeg);
        rightLowerLeg = new RigBone(humanoid, HumanBodyBones.RightLowerLeg);

        // hips = new RigBone(humanoid, HumanBodyBones.Hips);
    }
    void Update()
    {
        // LEFT
        leftUpperArm.set((float)(Langle[1] - 90.0f), 1, 0, 0);
        leftLowerArm.set((float)(180.0f - Langle[0]), 1, 0, 0);
        
        leftUpperLeg.offset((float)(Langle[2]-180.0f),0,0,1);
        leftLowerLeg.set((float)(-1.0f * Langle[3] - 180.0f), 0, 0, 1);

        // RIGHT
        rightUpperArm.set((float)(Rangle[1] - 90.0f), 1, 0, 0);
        rightLowerArm.set((float)(-1.0f * (180.0f - Rangle[0])), 1, 0, 0);

        rightUpperLeg.offset((float)(Rangle[2] - 180.0f),0,0,1);
        rightLowerLeg.set((float)(-1.0f * (Rangle[3] - 180.0f)), 0, 0, 1);

        // hips.set((float)(hipA), 1, 0, 0);

        humanoid.transform.rotation
          = Quaternion.AngleAxis(bodyRotation.z, new Vector3(0, 0, 1))
          * Quaternion.AngleAxis(bodyRotation.x, new Vector3(1, 0, 0))
          * Quaternion.AngleAxis(bodyRotation.y, new Vector3(0, 1, 0));
    }

    private void init()
    {
        print("UPDSend.init()");

        port = 5065;

        print("Sending to 127.0.0.1 : " + port);

        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("10.0.0.229"), port);
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);
                print(">> " + text);
                lastReceivedUDPPacket = text;
                allReceivedUDPPackets = allReceivedUDPPackets + text;

                if (partNum == 0){
                    Langle[0] = float.Parse(text);
                }

                if (partNum == 1){
                    Langle[1] = float.Parse(text);
                }

                if (partNum == 2){
                    Langle[2] = float.Parse(text);
                }

                if (partNum == 3){
                    Langle[3] = float.Parse(text);
                }

                if (partNum == 4){
                    Rangle[0] = float.Parse(text);
                }

                if (partNum == 5){
                    Rangle[1] = float.Parse(text);
                }

                if (partNum == 6){
                    Rangle[2] = float.Parse(text);
                }

                if (partNum == 7){
                    Rangle[3] = float.Parse(text);
                }

                // Cycle through the 3 data points
                partNum = partNum + 1;
                if (partNum == 8)
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

    void OnGUI()
    {
        Rect rectObj = new Rect(40, 10, 200, 400);
        GUIStyle style = new GUIStyle();
        style.alignment = TextAnchor.UpperLeft;
        GUI.Box(rectObj, "# UDPReceive\n127.0.0.1 " + port + " #\n"
                  + "\nLast Packet: \n" + lastReceivedUDPPacket
                  , style);
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
