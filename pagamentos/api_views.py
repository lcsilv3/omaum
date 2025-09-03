"""
API views para o app Pagamentos - REST padronizado
"""

import importlib
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import Http404


class PagamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar pagamentos
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Importação dinâmica do serializer"""
        try:
            serializers_module = importlib.import_module("pagamentos.serializers")
            return getattr(serializers_module, "PagamentoSerializer")
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar PagamentoSerializer: {e}")

    def get_service(self):
        """Importação dinâmica do service"""
        try:
            services_module = importlib.import_module("pagamentos.services")
            return getattr(services_module, "PagamentoService")()
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar PagamentoService: {e}")

    def get_queryset(self):
        """Retorna queryset através do service"""
        service = self.get_service()
        return service.get_all_pagamentos()

    def list(self, request):
        """Lista todos os pagamentos"""
        try:
            service = self.get_service()
            pagamentos = service.get_all_pagamentos()
            serializer = self.get_serializer_class()(pagamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao listar pagamentos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """Retorna um pagamento específico"""
        try:
            service = self.get_service()
            pagamento = service.get_pagamento_by_id(pk)
            if not pagamento:
                raise Http404("Pagamento não encontrado")
            serializer = self.get_serializer_class()(pagamento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"error": "Pagamento não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar pagamento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @transaction.atomic
    def create(self, request):
        """Cria um novo pagamento"""
        try:
            service = self.get_service()
            serializer = self.get_serializer_class()(data=request.data)

            if serializer.is_valid():
                pagamento = service.create_pagamento(serializer.validated_data)
                response_serializer = self.get_serializer_class()(pagamento)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Erro ao criar pagamento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @transaction.atomic
    def update(self, request, pk=None):
        """Atualiza um pagamento existente"""
        try:
            service = self.get_service()
            pagamento = service.get_pagamento_by_id(pk)
            if not pagamento:
                raise Http404("Pagamento não encontrado")

            serializer = self.get_serializer_class()(pagamento, data=request.data)
            if serializer.is_valid():
                pagamento_atualizado = service.update_pagamento(
                    pk, serializer.validated_data
                )
                response_serializer = self.get_serializer_class()(pagamento_atualizado)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"error": "Pagamento não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao atualizar pagamento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @transaction.atomic
    def destroy(self, request, pk=None):
        """Remove um pagamento"""
        try:
            service = self.get_service()
            pagamento = service.get_pagamento_by_id(pk)
            if not pagamento:
                raise Http404("Pagamento não encontrado")

            service.delete_pagamento(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {"error": "Pagamento não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao deletar pagamento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        """Confirma um pagamento"""
        try:
            service = self.get_service()
            pagamento = service.get_pagamento_by_id(pk)
            if not pagamento:
                raise Http404("Pagamento não encontrado")

            data_pagamento = request.data.get("data_pagamento")
            pagamento_confirmado = service.confirmar_pagamento(pk, data_pagamento)
            serializer = self.get_serializer_class()(pagamento_confirmado)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"error": "Pagamento não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao confirmar pagamento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        """Cancela um pagamento"""
        try:
            service = self.get_service()
            pagamento = service.get_pagamento_by_id(pk)
            if not pagamento:
                raise Http404("Pagamento não encontrado")

            motivo = request.data.get("motivo")
            pagamento_cancelado = service.cancelar_pagamento(pk, motivo)
            serializer = self.get_serializer_class()(pagamento_cancelado)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {"error": "Pagamento não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao cancelar pagamento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def por_aluno(self, request):
        """Lista pagamentos por aluno"""
        try:
            aluno_id = request.query_params.get("aluno_id")
            if not aluno_id:
                return Response(
                    {"error": "Parâmetro aluno_id é obrigatório"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            service = self.get_service()
            pagamentos = service.get_pagamentos_by_aluno(aluno_id)
            serializer = self.get_serializer_class()(pagamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar pagamentos por aluno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def por_turma(self, request):
        """Lista pagamentos por turma"""
        try:
            turma_id = request.query_params.get("turma_id")
            if not turma_id:
                return Response(
                    {"error": "Parâmetro turma_id é obrigatório"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            service = self.get_service()
            pagamentos = service.get_pagamentos_by_turma(turma_id)
            serializer = self.get_serializer_class()(pagamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar pagamentos por turma: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def por_status(self, request):
        """Lista pagamentos por status"""
        try:
            status_param = request.query_params.get("status")
            if not status_param:
                return Response(
                    {"error": "Parâmetro status é obrigatório"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            service = self.get_service()
            pagamentos = service.get_pagamentos_by_status(status_param)
            serializer = self.get_serializer_class()(pagamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar pagamentos por status: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def vencidos(self, request):
        """Lista pagamentos vencidos"""
        try:
            service = self.get_service()
            pagamentos = service.get_pagamentos_vencidos()
            serializer = self.get_serializer_class()(pagamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar pagamentos vencidos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def por_periodo(self, request):
        """Lista pagamentos por período"""
        try:
            data_inicio = request.query_params.get("data_inicio")
            data_fim = request.query_params.get("data_fim")

            if not data_inicio or not data_fim:
                return Response(
                    {"error": "Parâmetros data_inicio e data_fim são obrigatórios"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            service = self.get_service()
            pagamentos = service.get_pagamentos_by_periodo(data_inicio, data_fim)
            serializer = self.get_serializer_class()(pagamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao buscar pagamentos por período: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def total(self, request):
        """Calcula total de pagamentos"""
        try:
            service = self.get_service()
            total = service.calcular_total_pagamentos(
                aluno_id=request.query_params.get("aluno_id"),
                turma_id=request.query_params.get("turma_id"),
                status=request.query_params.get("status"),
            )
            return Response(total, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao calcular total: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def relatorio(self, request):
        """Gera relatório de pagamentos"""
        try:
            service = self.get_service()
            relatorio = service.gerar_relatorio_pagamentos(request.query_params.dict())
            return Response(relatorio, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Erro ao gerar relatório: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
