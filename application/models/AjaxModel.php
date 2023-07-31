<?php
class AjaxModel extends CI_Model 
{  
    public function saveData($data) 
	{
		if($this->db->insert('student',$data))
		{
		return 1;	
		}
		else
		{
		return 0;	
		}
    }
}
?>