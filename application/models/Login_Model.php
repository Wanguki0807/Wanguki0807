<?php
class Login_Model extends CI_Model 
{
	function checkemail($email,$pass)
	{
        $query=$this->db->query("select * from student where email ='".$email."' and password ='".$pass."';");
        $rowNum = $query->num_rows();
        if($rowNum)
            {
                $data['error']="<h3 style='color:blue'>Ok, you have Entered</h3>";
                $this->load->view('dashboard');
            }    
        else
        {
            $data['error']="<h3 style='color:red'> Email or Password was wrong. Please type again</h3>";
            $this->load->view('login',@$data);
        }

	}

	
}