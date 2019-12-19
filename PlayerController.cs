using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    bool loaded = false;

    public struct Player
    {
        public int id;
        public string username;

        public Stats playerStats;

        public string[] skills;
    };

    public struct Stats
    {
        public int strength;
        public int dexterity;
        public int wizardry;
        public int constitution;
    };

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Move()
    {

    }
}
