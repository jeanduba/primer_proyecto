### Diagrama de Flujo de la Calculadora

```mermaid
graph TD
    %% Inicio del programa
    Start([Inicio del Programa]) --> Welcome[/Bienvenido <br> Coloque lo que desea calcular/]
    Welcome --> Node2((2))

    %% Ciclo principal
    Node2 --> InputNums[/Ingresar n1 y n2/]
    InputNums --> Process[Suma = n1 + n2 <br> Resta = n1 - n2 <br> Multiplicación = n1 * n2 <br> División = n1 / n2]
    Process --> InputOp[/Ingresar tipo de operación <br> + , - , * , / /]

    %% Estructura de decisión (Operaciones)
    InputOp --> IsSum{Es +}
    IsSum -- Sí --> ResSum[/Resultado de la Suma/]
    
    IsSum -- No --> IsSub{Es -}
    IsSub -- Sí --> ResSub[/Resultado de la Resta/]
    
    IsSub -- No --> IsMult{Es *}
    IsMult -- Sí --> ResMult[/Resultado de la Multiplicación/]
    
    IsMult -- No --> IsDiv{Es /}
    
    %% Validación de división por cero
    IsDiv -- Sí --> CheckZero{n2 = 0}
    CheckZero -- Sí --> Error[/ERROR: No se puede dividir entre 0/]
    Error --> Node1((1))
    Node1 --> InputNums
    
    CheckZero -- No --> ResDiv[/Resultado de la División/]

    %% Fin del ciclo / Reinicio
    ResSum --> AskNext[/¿Hacer otro cálculo?/]
    ResSub --> AskNext
    ResMult --> AskNext
    ResDiv --> AskNext

    AskNext --> Choice{Otro cálculo}
    Choice -- Sí --> Node2
    Choice -- No --> EndMsg[/Fin/]
    EndMsg --> End([Fin del Programa])’’’
