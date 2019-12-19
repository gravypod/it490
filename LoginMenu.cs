using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class LoginMenu : MonoBehaviour
{

    public InputField username, password;
    public Button login, createAccount, move;
    public GameObject loginPanel;

    [HideInInspector]
    public PlayerController.Player player;

    

    struct Login
    {
        public string username;
        public string password;
    }

    // Start is called before the first frame update
    void Start()
    {
        login.onClick.AddListener(UserLogin);
        createAccount.onClick.AddListener(CreateAccount);


        move.onClick.AddListener(HideLoginMenu);

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void UserLogin()
    {
        

        if(username.text == null)
        {
            //no login - break
        }
        else if (password.text == null)
        {
            //no login - break
        }

        StartCoroutine(LoginCoroutine());

    }
    void CreateAccount()
    {
        if (username.text == null)
        {
            //no login - break
        }
        else if (password.text == null)
        {
            //no login - break
        }

        StartCoroutine(CreateAccountCoroutine());
    }

    void HideLoginMenu()
    {
        
        StartCoroutine(HideLoginMenuCoroutine());
    }

    IEnumerator HideLoginMenuCoroutine()
    {
        //raise 500 then hide it

        Vector2 vec2 = new Vector2(loginPanel.transform.position.x, loginPanel.transform.position.y);
        vec2 += new Vector2(0f, 500f);

        while (loginPanel.transform.position.y != vec2.y)
        {
            loginPanel.transform.position = Vector2.Lerp(loginPanel.transform.position, vec2, Time.deltaTime*2);
            yield return null;
        }

        loginPanel.SetActive(false);
        StopCoroutine(HideLoginMenuCoroutine());
    }

    IEnumerator LoginCoroutine()
    {
        //rabbitmq.it490.localhost 
        string loginInfoStr;

        Login login = new Login();

        login.username = username.text;
        login.password = password.text;

        loginInfoStr = JsonUtility.ToJson(login);


        WWWForm dataForm = new WWWForm();
       

        dataForm.AddField("login", loginInfoStr);

        using (UnityWebRequest send = UnityWebRequest.Post("gateway.it490.localhost/logins", dataForm))
        {
            DownloadHandler download = send.downloadHandler;
            yield return send.SendWebRequest();

            if (send.isNetworkError || send.isHttpError)
                Debug.Log(send.error);
            else
            {
                if (download.isDone)
                {
                    string tempStr = download.text;

                    player = JsonUtility.FromJson<PlayerController.Player>(tempStr);
                    //StartCoroutine(LoadData());
                }
            }
        }
    }

    IEnumerator CreateAccountCoroutine()
    {
        string createInfoStr;

        Login newLogin = new Login();

        newLogin.username = username.text;
        newLogin.password = password.text;

        createInfoStr = JsonUtility.ToJson(login);


        WWWForm dataForm = new WWWForm();

        dataForm.AddField("create", createInfoStr);

        using (UnityWebRequest send = UnityWebRequest.Post("gateway.it490.localhost/players", dataForm))
        {
            DownloadHandler download = send.downloadHandler;
            yield return send.SendWebRequest();

            if (send.isNetworkError || send.isHttpError)
                Debug.Log(send.error);
            else
            {
                if (download.isDone)
                {
                    string tempStr = download.text;
                    
                    player = JsonUtility.FromJson<PlayerController.Player>(tempStr);
                    //StartCoroutine(LoadData());
                }
            }
                //StartCoroutine(LoadData());
        }
    }

   //IEnumerator LoadData()
   // {
   //     string playerData;
   //     HideLoginMenu();

   //     using (UnityWebRequest getter = UnityWebRequest.Get("gateway.it490.localhost/player_login"))
   //     {
   //         yield return getter.SendWebRequest();

   //         if (getter.isNetworkError || getter.isHttpError)
   //         {
   //             Debug.Log(getter.error);

   //         }
   //         else
   //         {
   //             playerData = getter.downloadHandler.text;
   //             PlayerController.Player player = new PlayerController.Player();
   //             player = JsonUtility.FromJson<PlayerController.Player>(playerData);
   //         }
   //     }
                
   // }
    

}
