import matplotlib.pyplot as plt

def find_between(s, first, last):

	try:
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""

def file_cropper(filepremium, filetrash):

	premium_values = []
	trash_values = []

	with open(filepremium, 'rb') as fp:

		for line in fp:

			temp_text = line.replace(" ", "")

			if "TXpackets" in temp_text:
				bytes_premium = find_between(temp_text, "bytes", "(").split('/')
				bytes_premium = bytes_premium[0]
				premium_values.append(bytes_premium)

	with open(filetrash, 'rb') as ft:

		for line in ft:

			temp_text = line.replace(" ", "")

			if "TXpackets" in temp_text:
				bytes_trash = find_between(temp_text, "bytes", "(").split('/')
				bytes_trash = bytes_trash[0]
				trash_values.append(bytes_trash)

	temp_premium_values = []
	temp_trash_values = []

	results = []

	for index in range(0, len (premium_values), 10):

		if(len (premium_values) - index < 10):
			break

		temp_premium = (premium_values[index: index + 10])
		temp_premium_values.append(sum(int(i) for i in temp_premium))

		temp_trash = trash_values[index: index + 10]
		temp_trash_values.append(sum(int(i) for i in temp_trash))

	list_premium = []
	list_trash = []

	for index in range(len(temp_premium_values)):

		if(index == 0):

			premiumbytes = temp_premium_values[index]
			list_premium.append(premiumbytes)
			trashbytes = temp_trash_values[index]
			list_trash.append(trashbytes)

		else:

			premiumbytes = temp_premium_values[index] - temp_premium_values[index - 1]
			list_premium.append(premiumbytes)
			trashbytes = temp_trash_values[index] - temp_trash_values[index - 1]
			list_trash.append(trashbytes)

	for index in range(len(temp_premium_values)):

		premiumbytes = list_premium[index]
		trashbytes = list_trash[index]

		if((premiumbytes == 0) or (trashbytes >= premiumbytes)):
			results.append(100)

		else:

			if(((trashbytes * 100) / premiumbytes) >= 100):
				results.append(100)

			else:
				results.append((trashbytes * 100) / premiumbytes)

	return results

def main ():

	first_set = file_cropper("ctn11_net_stats.txt", "ctn16_net_stats.txt")
	second_set = file_cropper("ctn12_net_stats.txt", "ctn17_net_stats.txt")
	third_set = file_cropper("ctn13_net_stats.txt", "ctn18_net_stats.txt")
	fourth_set = file_cropper("ctn14_net_stats.txt", "ctn19_net_stats.txt")
	fifth_set = file_cropper("ctn15_net_stats.txt", "ctn20_net_stats.txt")

	x1_Trash = [1]
	x2_Trash = [6]
	x3_Trash = [10]
	x4_Trash = [14]
	x5_Trash = [19]

	x_Premium = [1]
	y_Premium = [100]

	for index in range (2, 31):
		x1_Trash.append(index)

	for index in range (7, 31):
		x2_Trash.append(index)

	for index in range (11, 31):
		x3_Trash.append(index)

	for index in range (15, 31):
		x4_Trash.append(index)

	for index in range (20, 31):
		x5_Trash.append(index)

	for index in range (1, 31):
		x_Premium.append(index)
		y_Premium.append(100)

	x_axis = [1, 5, 10, 15, 20, 25, 30]

	fig, ax = plt.subplots()

	ax.plot(x_Premium, y_Premium, color='black', marker='o', markerfacecolor='black', markersize = 14, label="Premium service")
	ax.plot(x1_Trash, first_set, color='b', marker='s', markersize = 14, label="BE service 1")
	ax.plot(x2_Trash, second_set, color='r', marker='D', markersize = 14, label="BE service 2")
	ax.plot(x3_Trash, third_set, color='g', marker='d', markersize = 14, label="BE service 3")
	ax.plot(x4_Trash, fourth_set, color='m', marker='v', markersize = 14, label="BE service 4")
	ax.plot(x5_Trash, fifth_set, color='orange', marker='^', markersize = 14, label="BE service 5")

	y_axis = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
	plt.xticks(x_axis)
	plt.yticks(y_axis)
	plt.xlabel('Time window (10 sec.)', fontsize = 33)
	plt.ylabel('Quality of service (%)', fontsize = 33)
	plt.tick_params(labelsize = 33)
	plt.legend(fontsize = 28, loc='lower left')
	ax = plt.gca()
	ax.grid(axis='y')
	plt.show()

if __name__ == '__main__':
	main()