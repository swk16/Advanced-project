using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class switch9 : MonoBehaviour
{
    // Start is called before the first frame update
   private void OnCollisionEnter(Collision other) {
    
    if (other.gameObject.tag == "fire") {
        SceneManager.LoadScene("Thunder");
        
    }
} 
}
