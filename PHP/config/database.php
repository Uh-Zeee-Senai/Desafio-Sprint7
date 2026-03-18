<?php
class Database {
    private static $host = "localhost";
    private static $db_name = "cadastro_eventos";
    private static $username = "root";
    private static $password = "";
    private static $instance = null;

    public static function getConnection() {
        if (!self::$instance) {
            try {
                self::$instance = new PDO(
                    "mysql:host=" . self::$host . ";port=3308;dbname=" . self::$db_name . ";charset=utf8",
                    self::$username,
                    self::$password
                );
                self::$instance->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            } catch (PDOException $e) {
                die("Erro na conexão: " . $e->getMessage());
            }
        }
        return self::$instance;
    }
}