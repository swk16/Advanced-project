using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class switch6 : MonoBehaviour
{
    // Start is called before the first frame update
   private void OnCollisionEnter(Collision other) {
    
    if (other.gameObject.tag == "metal") {
        
        SceneManager.LoadScene("heaven");

    }
} 
}
