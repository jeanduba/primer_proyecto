``` mermaid

graph TD
    Inicio([INICIO DEL PROGRAMA]) --> Bienvenida[/BIENVENIDO <br> COLOQUE LO QUE DESEA CALCULAR/]
    
    Bienvenida --> Procesos[Suma = n1 + n2 <br> Resta = n1 - n2 <br> Multiplicación = n1 * n2 <br> División = n1 / n2]
    
    Procesos --> IngresarN[/INGRESAR n1 y n2/]
    
    IngresarN --> TipoOp[/INGRESAR TIPO DE OPERACIÓN <br> + , - , * , //]
    
    TipoOp --> EsSuma{ES +}
    
    EsSuma -- SI --> ResSuma[/RESULTADO DE LA SUMA/]
    EsSuma -- NO --> EsResta{ES -}
    
    EsResta -- SI --> ResResta[/RESULTADO DE LA RESTA/]
    EsResta -- NO --> EsMult{ES *}
    
    EsMult -- SI --> ResMult[/RESULTADO DE LA MULTIPLICACIÓN/]
    EsMult -- NO --> EsDiv{ES /}
    
    EsDiv -- SI --> CheckCero{n2 = 0}
    
    CheckCero -- NO --> ResDiv[/RESULTADO DE LA DIVISIÓN/]
    CheckCero -- SI --> Error[/ERROR: DIVISIÓN POR CERO/]
    
    ResSuma --> OtroCalc[/¿HACER OTRO CÁLCULO?/]
    ResResta --> OtroCalc
    ResMult --> OtroCalc
    ResDiv --> OtroCalc
    Error --> OtroCalc
    
    OtroCalc --> Decidir{OTRO CÁLCULO}
    
    Decidir -- SI --> Bienvenida
    Decidir -- NO --> Fin[/FIN/]
    
    Fin --> Terminar([FIN DEL PROGRAMA])


  