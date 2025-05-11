command.append('tests.performance')
        elif test_type == 'security':
            command.append('tests.security')
        else:
            print(f"Tipo de teste desconhecido: {test_type}")
            return False
    
    if coverage:
        # Substituir o comando para usar o coverage
        command = ['coverage', 'run', '--source=.'] + command[1:]
    
    if verbose:
        command.append('-v')
    
    print(f"Executando comando: {' '.join(command)}")
    start_time = time.time()
    result = subprocess.run(command, capture_output=not verbose)
    end_time = time.time()
    
    if result.returncode != 0:
        print("Falha na execução dos testes!")
        if not verbose:
            print(result.stderr.decode('utf-8'))
        return False
    
    print(f"Testes executados com sucesso em {end_time - start_time:.2f} segundos!")
    
    if coverage:
        print("Gerando relatório de cobertura...")
        subprocess.run(['coverage', 'report'])
        subprocess.run(['coverage', 'html'])
        print("Relatório HTML gerado em htmlcov/index.html")
    
    return True

def generate_report(output_file, module=None, test_type=None):
    """Generate a test report and save it to the specified file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w') as f:
        f.write(f"# Relatório de Testes - Sistema OMAUM\n\n")
        f.write(f"Data/Hora: {timestamp}\n\n")
        
        if module:
            f.write(f"Módulo: {module}\n")
        if test_type:
            f.write(f"Tipo de Teste: {test_type}\n")
        
        f.write("\n## Resultados\n\n")
        
        # Executar testes e capturar saída
        command = ['python', 'manage.py', 'test', '--settings=config.settings.test']
        
        if module and test_type:
            command.append(f'tests.{module}.test_{test_type}')
        elif module:
            command.append(f'tests.{module}')
        elif test_type:
            if test_type in ['e2e', 'performance', 'security']:
                command.append(f'tests.{test_type}')
            else:
                modules = ['alunos', 'turmas', 'atividades', 'frequencias', 'notas', 'pagamentos', 'matriculas']
                if test_type == 'unit':
                    test_modules = [f'tests.{m}.test_models tests.{m}.test_forms' for m in modules]
                elif test_type == 'integration':
                    test_modules = [f'tests.{m}.test_views' for m in modules]
                command.append(' '.join(test_modules))
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            f.write("✅ Todos os testes passaram com sucesso!\n\n")
        else:
            f.write("❌ Alguns testes falharam.\n\n")
        
        f.write("### Detalhes\n\n")
        f.write("\n")
        f.write(result.stdout)
        f.write("\n\n\n")
        
        if result.returncode != 0:
            f.write("### Erros\n\n")
            f.write("\n")
            f.write(result.stderr)
            f.write("\n\n")
    
    print(f"Relatório gerado em {output_file}")
    return True

def main():
    """Main function."""
    args = parse_args()
    
    if not args.module and not args.type and not args.all:
        print("Erro: Você deve especificar um módulo, um tipo de teste ou a flag --all")
        return 1
    
    if args.output:
        return 0 if generate_report(args.output, args.module, args.type) else 1
    else:
        return 0 if run_tests(args.module, args.type, args.coverage, args.verbose) else 1

if __name__ == "__main__":
    sys.exit(main())