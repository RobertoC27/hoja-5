from SimPy.Simulation import *
from random import uniform, Random
class Procesos(Process):
	def __init__(self,id):
		Process.__init__(self)
		self.nombre=id

	def ejecutar(self,cantRAM,cantInstrucciones):
		if Memoria>=cantRAM:
			self.RAM=cantRAM		
			print "El proceso", self.nombre ,"solicita ", self.RAM ," MB de RAM"
			yield request
		else:
			print "No hay suficiente memoria para el proceso", self.nombre
		self.cantInstrucciones=cantInstrucciones
		i=3
		yield request,self,ready
		print self.nombre, "está listo para ser atendido por el cpu"
		while(self.cantInstrucciones>0):
			yield release,self,ready
			if (self.cantInstrucciones-i)<=0:
				print "No se necesitan más de 1 ciclo para el proceso",self.nombre , "usa ",self.cantInstrucciones, "instrucciones" 
				yield request, self, cpu
				print self.nombre, "obtiene cpu"
				self.cantInstrucciones=self.cantInstrucciones-i
				i=i+1
				yield release, self, cpu
				print self.nombre, "libera cpu"
				
				
				
				
			else:
				print "Se necesitan más de 1 ciclo para el proceso",self.nombre, "usa ",self.cantInstrucciones
				yield request, self, cpu
				self.cantInstrucciones=self.cantInstrucciones-i
				i=i+1
				yield release, self, cpu
				decision=azar.randint(1,2+1)
					if decision==1:
						yield request,self,waiting
						yield hold,self,1
						yield release,self,waiting
					
					else:
						yield request,self,ready
					
				


initialize() #inicar la simulacion. Tiempo = 0
nrCars=1
cpu = Resource(capacity=1)
azar = Random(12345) #se puede reproducir los mismos numeros al azar
parkingLot=Resource(capacity=4,qType=FIFO)
#memoria = container(init=100,capacity=100)
Memoria= Resource(capacity=100)
ready=Resource(capacity=20,qType=FIFO)
waiting=Resource(capacity=20,qType=FIFO)


for i in range(nrCars):
    c=Procesos(id="Proceso #"+ str(i)) #se crea una instancia por cada carro
    #activar los carros en la lista de simulacion. Se genera un numero
    #al azar para indicar el tiempo que se conduce cada carro para llegar
    #a la meta.
    activate(c,c.ejecutar(cantRAM=azar.randint(1,10+1),cantInstrucciones=azar.randint(1,10+1)))
    
simulate(until=100) #simular para 100 unidades de tiempo
