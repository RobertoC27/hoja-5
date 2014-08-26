from SimPy.Simulation import *
from random import uniform, Random
class Procesos(Process):
	def __init__(self,id):
		Process.__init__(self)
		self.nombre=id

	def ejecutar(self,cantRAM,cantInstrucciones):
		self.llega= now() #tiempo de ingreso del proceso
		if Memoria>=cantRAM:
			self.RAM=cantRAM		
			print "El proceso", self.nombre ,"solicita ", self.RAM ," MB de RAM"
			
		else:
			print "No hay suficiente memoria para el proceso", self.nombre
		self.cantInstrucciones=cantInstrucciones
		i=3
		yield request,self,ready
		print self.nombre, "en cola para ser atendido por el cpu"
		while(self.cantInstrucciones>0):
			yield release,self,ready
			print self.nombre, "está listo para ser atendido por el cpu"
			
			if (self.cantInstrucciones-i)<=0:#mira si puede resolver las instrucciones con una solo llegada al cpu
				print "No se necesitan más de 1 ciclo para ",self.nombre , ", usa ",self.cantInstrucciones, "instrucciones" 
				yield request, self, cpu
				print self.nombre, "obtiene cpu"
				self.cantInstrucciones=self.cantInstrucciones-i
				i=i+1
				yield release, self, cpu
				tiempoProceso= now() - self.llega
				wt.observe(tiempoProceso)
				print self.nombre, "libera cpu"
				print self.nombre, "sale del sistema"
					
			else:#si se necesita más de una llegada al cpu para resolver el proceso
				print "Se necesitan más de 1 ciclo para el proceso",self.nombre, "usa ",self.cantInstrucciones, "instrucciones" 
				yield request, self, cpu
				print self.nombre, "obtiene cpu"
				self.cantInstrucciones=self.cantInstrucciones-i
				i=i+1
				yield release, self, cpu
				print self.nombre, "libera cpu"
				decision=random.randint(1,2+1)
				if decision==1: #entra a la cola de waiting
					yield request,self,waiting
					print self.nombre, "está en espera para ser atendido por el cpu"
					yield hold,self,1
					print self.nombre, "sale de espera para ser atendido por el cpu"
					yield release,self,waiting
					yield request,self,ready
					print self.nombre, "en cola para ser atendido por el cpu"
				
				else: #regresa al estado de ready
					yield request,self,ready
					print self.nombre, "en cola para ser atendido por el cpu"
				


wt=Monitor()
initialize() #inicar la simulacion. Tiempo = 0
nrCars=10
cpu = Resource(capacity=1)
#azar = Random() #se puede reproducir los mismos numeros al azar
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
    activate(c,c.ejecutar(cantRAM=random.randint(1,10+1),cantInstrucciones=random.randint(1,10+1)))
    
simulate(until=100) #simular para 100 unidades de tiempo

print "Tiempo total de los procesos: \tmean = %5.1f, \n\t\tvariance=%2d"%(wt.mean(),wt.var())
