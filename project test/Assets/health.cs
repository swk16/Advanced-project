using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class health : MonoBehaviour
{
    [SerializeField] protected float maxHealth=4;

    float healthtimes;

    private MeshRenderer m_meshrenderer;
 
	// Use this for initialization
	void Start () {
        m_meshrenderer = gameObject.GetComponent<MeshRenderer>();
        //StartCoroutine(healthtimes());

	}
	
	
	private void OnCollisionEnter(Collision other) {
    
    if (other.gameObject.tag == "water") {
        healthtimes = healthtimes + 1;
        other.gameObject.SetActive(false);

        if (healthtimes == 1) {
            m_meshrenderer.material.color = Color.red;
        }
        if (healthtimes == 2) {
            m_meshrenderer.material.color = Color.yellow;
        }
        if (healthtimes == 3) {
            m_meshrenderer.material.color = Color.green;
        }
        if (healthtimes == 4) {
            
            StartCoroutine(TimeDelay());
            
        }
    }

    }
    IEnumerator TimeDelay()
    {
        yield return new WaitForSeconds(2);
        gameObject.SetActive(false);
        
        SceneManager.LoadScene("start");
    }

}  
 




  


