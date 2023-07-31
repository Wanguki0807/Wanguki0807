<?php
class User extends CI_Controller 
{
	public function __construct()
	{
	parent::__construct();
	$this->load->database();
	$this->load->helper('url');
	}

	public function registers()
	{
		$this->load->view('student_registration');
		if($this->input->post('register'))
		{
		$n=$this->input->post('name');
		$e=$this->input->post('email');
		$p=$this->input->post('pass');
		$m=$this->input->post('mobile');
		$c=$this->input->post('course');

		$this->load->model('Register_Model');
		$this->form_validation->set_rules('name', 'Name', 'trim|required|min_length[4]|max_length[10]');
		$this->form_validation->set_rules('email', 'Email', 'required|valid_email|is_unique[users.email]');

		$this->Register_Model->registerInfo($n,$e,$p,$m,$c);
		
		}	
		
	}

    public function login()
    {
        if($this-> input->post('login'))
        {
            $e = $this->input->post('email');
            $p = $this->input->post('pass');
			$this->load->model('Login_Model');
			$this->Login_Model->checkemail($e,$p);
		}
   
		
    }


}
?>