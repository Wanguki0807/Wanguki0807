<?php
class StudentPagination_Model extends CI_Model 
{
    public function get_count() 
	{
        return $this->db->count_all("student");
    }

    public function get_students($limit, $start) 
	{
        $this->db->limit($limit, $start);
        $query = $this->db->get("student");
        return $query->result();
    }
}
?>