<?php
class Evento {
    private $conn;
    private $table = "eventos";

    public $id_evento;
    public $titulo;
    public $descricao;
    public $data_evento;
    public $local_evento;
    public $preco;

    public function __construct($db) {
        $this->conn = $db;
    }
    public function listar() {
        $query = "SELECT * FROM " . $this->table . " ORDER BY data_evento ASC";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }
    public function criar() {
        $query = "INSERT INTO " . $this->table . "
                  (titulo, descricao, data_evento, local_evento, preco)
                  VALUES (:titulo, :descricao, :data_evento, :local_evento, :preco)";

        $stmt = $this->conn->prepare($query);

        $stmt->bindParam(":titulo", $this->titulo);
        $stmt->bindParam(":descricao", $this->descricao);
        $stmt->bindParam(":data_evento", $this->data_evento);
        $stmt->bindParam(":local_evento", $this->local_evento);
        $stmt->bindParam(":preco", $this->preco);

        return $stmt->execute();
    }

    public function deletar() {
        $query = "DELETE FROM " . $this->table . " WHERE id_evento = :id";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(":id", $this->id_evento);
        return $stmt->execute();
    }
}