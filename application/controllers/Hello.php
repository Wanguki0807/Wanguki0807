<?php
class Hello extends CI_Controller 
{
	public function __construct()
	{
	//call CodeIgniter's default Constructor
	parent::__construct();
	$this->load->database();
	$this->load->helper('url');
    $this->load->model('Hello_Model');
	}

	public function savedata()
	{
		$this->load->view('registration');
		if($this->input->post('save'))
		{
            $n=$this->input->post('name');
            $e=$this->input->post('email');
            $m=$this->input->post('mobile');
            $this->Hello_Model->saverecords($n,$e,$m);		
            echo "Records Saved Successfully";
        }
	}

    public function dispdata()
	{
        $result['data']=$this->Hello_Model->displayrecords();
        $this->load->view('display_records',$result);
	}

    public function deletedata()
	{
        $id=$this->input->get('id');
        $this->Hello_Model->deleterecords($id);
        redirect("Hello/dispdata");
	}

    public function updatedata()
	{
        $id=$this->input->get('id');
        $result['data']=$this->Hello_Model->displayrecordsById($id);
        $this->load->view('update_records',$result);	
        
		if($this->input->post('update'))
		{
            $n=$this->input->post('name');
            $e=$this->input->post('email');
            $m=$this->input->post('mobile');
            $this->Hello_Model->updaterecords($n,$e,$m,$id);
            redirect("Hello/dispdata");
		}
	}
}
?>