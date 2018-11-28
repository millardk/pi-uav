package base;

import com.github.strikerx3.jxinput.XInputDevice14;

import com.digi.xbee.api.RemoteXBeeDevice;
import com.digi.xbee.api.XBeeDevice;
import com.digi.xbee.api.XBeeNetwork;
import com.digi.xbee.api.listeners.IDataReceiveListener;
import com.digi.xbee.api.models.XBeeMessage;

abstract class  Channel {
    abstract public byte getOutput(XInputDevice14 device);
    abstract public byte getFallback();
}

class Controller {

    static Channel[] channels;
    static XInputDevice14 device;
    static byte[] lastOutput;

    static {
        Channel aileron = new Channel() {
            @Override
            public byte getOutput(XInputDevice14 device) {
                return (byte)(device.getComponents().getAxes().rxRaw >> 8);
            }
            @Override
            public byte getFallback() {
                return 127;
            }
        };

        Channel elevator = new Channel() {
            @Override
            public byte getOutput(XInputDevice14 device) {
                return (byte)(device.getComponents().getAxes().ryRaw >> 8);
            }
            @Override
            public byte getFallback() {
                return 127;
            }
        };

        Channel throttle = new Channel() {
            @Override
            public byte getOutput(XInputDevice14 device) {
                int raw = device.getComponents().getAxes().ltRaw;
                return (byte) (-128 + raw);
            }
            @Override
            public byte getFallback() {
                return 0;
            }
        };

        Channel rudder = new Channel() {
            @Override
            public byte getOutput(XInputDevice14 device) {
                return (byte)(device.getComponents().getAxes().lxRaw >> 8);
            }
            @Override
            public byte getFallback() {
                return 127;
            }
        };

        channels = new Channel[]{aileron, elevator, throttle, rudder};

        try {
            device = XInputDevice14.getAllDevices()[0];
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }

        lastOutput = getOutput();
    }

    public static byte[] getOutput(){
        byte[] out = new byte[channels.length];

        if(device.poll())
            for (int i = 0; i < channels.length; i++)
                out[i] = channels[i].getOutput(device);

        else
            for (int i = 0; i < channels.length; i++)
                out[i] = channels[i].getFallback();

        lastOutput = out;
        return out;
    }

    public static String stringRepr(){
        StringBuffer sb = new StringBuffer();
        for(byte c : lastOutput) {
            sb.append((int) c);
            sb.append(" ");
        }
        return sb.toString();
    }

}

class Downlink implements IDataReceiveListener {
    @Override
    public void dataReceived(XBeeMessage xBeeMessage){
        xBeeMessage.getData();
    }
}

public class Main {

    private static final String PORT = "COM4";
    private static final int BAUD_RATE = 9600;
    private static final String REMOTE_NODE_IDENTIFIER = "REMOTE";

    public static void main(String[] args) {
        try {
            XBeeDevice myDevice = new XBeeDevice(PORT, BAUD_RATE);
            myDevice.open();

            XBeeNetwork xbeeNetwork = myDevice.getNetwork();
            RemoteXBeeDevice remoteDevice = xbeeNetwork.discoverDevice(REMOTE_NODE_IDENTIFIER);
            if (remoteDevice == null) {
                System.out.println("Couldn't find the remote XBee device with '" + REMOTE_NODE_IDENTIFIER + "' Node Identifier.");
                System.exit(1);
            }

            Downlink downlink = new Downlink();
            myDevice.addDataListener(downlink);

            while (true) {
                byte[] data = Controller.getOutput();
                myDevice.sendDataAsync(remoteDevice, data);

                System.out.print(Controller.stringRepr()+'\r');
                Thread.sleep(50);
            }

        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }

    }

}








