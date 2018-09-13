from freeling import Freeling

# Load dataset as string
with open('../dataset/text.txt', 'r') as file:
	text = file.read()

analyzer = Freeling(language="es")
result = analyzer.run(text)

print(result[0][0].decode('utf8'))