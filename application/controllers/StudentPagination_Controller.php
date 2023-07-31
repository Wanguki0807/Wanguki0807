<?php defined('BASEPATH') OR exit('No direct script access allowed');

class StudentPagination_Controller extends CI_Controller {

    public function __construct() 
	{
        parent:: __construct();

        $this->load->helper('url','form');
        $this->load->library("pagination");
        $this->load->database();
		$this->load->model('StudentPagination_Model');
    }

    public function index() 
	{
        $config = array();
        $config["base_url"] = base_url() . "index.php/StudentPagination_Controller/index";
        $config["total_rows"] = $this->StudentPagination_Model->get_count();
        $config["per_page"] = 10;
        $config["uri_segment"] = 3;

        $this->pagination->initialize($config);

		
		$page = ($this->uri->segment(3))? $this->uri->segment(3) : 0;
		
        $data["links"] = $this->pagination->create_links();

        $data['student'] = $this->StudentPagination_Model->get_students($config["per_page"], $page);

        $this->load->view('pagination', $data);
    }
}
?>