package com.example.krys.traindroid;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

/**
 * This is a simple Android mobile client
 * This application read any string massage typed on the text field and
 * send it to the server when the Send button is pressed
 * Author by Lak J Comspace
 *
 */
public class MainActivity extends Activity {

    private Socket client;
    private PrintWriter printwriter;
    private DataInputStream diReader;
    private TextView textField;
    private Button button;
    private String message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textField = (TextView) findViewById(R.id.text_view_id); // reference to the text field
        button = (Button) findViewById(R.id.button1); // reference to the send button

        // Button press event listener
        button.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {
                //message = textField.getText().toString(); // get the text message on the text field
                //textField.setText(""); // Reset the text field to blank
                GetMessage getMessageTask = new GetMessage();
                getMessageTask.execute();
            }
        });
    }

    private class GetMessage extends AsyncTask<Void, Void, Void> {
        @Override
        protected Void doInBackground(Void... params) {
            try {
                client = new Socket("127.0.0.1", 10001); // connect to the server
                diReader = new DataInputStream(client.getInputStream());
                while(true){

                    while(message.length() < 32) {
                        message += diReader.readUTF();
                    }

                    try{
                        textField.setText(message);
                    }
                    catch( Exception e) {
                        e.printStackTrace();
                    }

                    //diReader.close();
                    //client.close(); // closing the connection
                }

            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        //getMenuInflater().inflate(R.menu.slimple_text_client, menu);
        return true;
    }

}
