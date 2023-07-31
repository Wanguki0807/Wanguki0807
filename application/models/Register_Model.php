<?php

class Register_Model extends CI_Model{

    function registerInfo($name,$email,$password,$mobile,$course)
    {

        $query = $this->db->get_where("student",array('email' =>$email));
		$row = $query->num_rows();
		if($row)
		{
		$data['error']="<h3 style='color:red'>This user already exists</h3>";
        // $this->load->view('student_registration',@$data);	
        redirect('User/registers',@$data);
		}
		else
		{
            $data = array('student_id'  => '',
                            'name'=>$name,
                            'email'=>$email,
                            'password'=>$password,
                            'mobile'=>$mobile,
                            'course'=>$course);
            $this->db->insert('student',$data);
            
	    	$data['error']="<h3 style='color:blue'>Your account created successfully</h3>";
            $this->load->view('dashboard',@$data);	
            // redirect('User/dashboard');
        }			
       
	}
}
?>