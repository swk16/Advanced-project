using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;          


public class switch_scene : MonoBehaviour
{
private void OnCollisionEnter(Collision other) {
    
    if (other.gameObject.tag == "fire") {
        SceneManager.LoadScene("Thunder");
    }
}                                                       
}

