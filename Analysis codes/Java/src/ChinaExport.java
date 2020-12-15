import tech.tablesaw.api.*;
import static tech.tablesaw.aggregate.AggregateFunctions.*;
import tech.tablesaw.table.*;
import tech.tablesaw.aggregate.*;
import tech.tablesaw.io.csv.CsvReadOptions;
import org.knowm.xchart.*;
import java.util.*;

public class ChinaExport {
    public static void main(String[] args) throws Exception{
        plot(groupIndicator(readCSV(getNames())));
    }

    //生成文件名列表，也可以dir
    public static String[] getNames(){
        var nameList=new ArrayList<String>();
        for(int year=2009;year<2019;year++){
            nameList.add("What did China export in "+year+"_");
        }
        var nameArray=new String[nameList.size()];
        nameList.toArray(nameArray);
        return nameArray;
    }

    //批量读取数据
    public static ArrayList<Table> readCSV (String[] nameArray) throws Exception{
        var STRING=ColumnType.STRING;
        var LONG=ColumnType.LONG;
        var DOUBLE=ColumnType.DOUBLE;
        var SKIP=ColumnType.SKIP;
        //设置column格式
        ColumnType[] types={STRING,LONG,DOUBLE,SKIP,STRING};
        var dataFrameList=new ArrayList<Table>();
        for(String name:nameArray){
            dataFrameList.add(Table.read().usingOptions(CsvReadOptions
                    .builder("C:/Users/92859/Desktop/CoreJava/data/"+name+".csv")
                    .columnTypes(types)));
        }
        var summarized=dataFrameList.get(0).summarize("Gross EXport","Share",sum).by("Sector");
        return dataFrameList;
    }

    //分组加总，合并年份，分类输出
    public static Table[] groupIndicator(ArrayList<Table> dataFrameList){
        var Export_Share=new Table[2];
        Table sumExport=Table.create("China Summarized Export Data for 2009~2018");
        Table sumShare=Table.create("China Summarized Export Share for 2009~2018");
        Integer year=2009;
        for(Table df:dataFrameList){
            var summarized=df.summarize("Gross EXport", "Share", sum).by("Sector");
            var sectorName=summarized.column("Sector");
            if(year==2009){
                sumExport.addColumns(sectorName);
                sumShare.addColumns(sectorName);
            }
            var export=summarized.column("Sum [Gross Export]").setName(Integer.toString(year));
            var share=summarized.column("Sum [Share]").setName(Integer.toString(year));
            sumExport.addColumns(export);
            sumShare.addColumns(share);
            year++;
        }
        Export_Share[0]=sumExport;
        Export_Share[1]=sumShare;
        System.out.println(Export_Share[0].print());
        System.out.println(Export_Share[1].print());
        return Export_Share;
    }

    //绘制分类折线图
    public static void plot(Table[] Export_Share) throws Exception{
        Table exportData=Export_Share[0];
        Table shareData=Export_Share[1];
        var xData=new double[10];
        for(int i=2009;i<2019;i++) xData[i-2009]=i;

        final XYChart exportChart = new XYChartBuilder().width(600).height(400).title("China Export for 2009~2018 in Categories").xAxisTitle("Year").yAxisTitle("Export").build();
        // for-loop手动生成行
        for(Row row:exportData){
            String exportCategory=row.getString("Sector");
            var valuesList=new ArrayList<Double>();
            for(int year=2009;year<2019;year++){
                valuesList.add(row.getDouble(Integer.toString(year)));
            }
            //利用流将 Double ArrayList 转基础类型 double[]
            double[] valuesArray = valuesList.stream().mapToDouble(i->i).toArray();
            exportChart.addSeries(exportCategory,xData,valuesArray);
        }
        new SwingWrapper(exportChart).displayChart();

        final XYChart shareChart = new XYChartBuilder().width(600).height(400).title("China Export Share for 2009~2018 in Categories").xAxisTitle("Year").yAxisTitle("Share").build();
        for(Row row:shareData){
            String shareCategory=row.getString("Sector");
            var valuesList=new ArrayList<Double>();
            for(int year=2009;year<2019;year++){
                valuesList.add(row.getDouble(Integer.toString(year)));
            }
            double[] valuesArray = valuesList.stream().mapToDouble(i->i).toArray();
            shareChart.addSeries(shareCategory,xData,valuesArray);
        }
        new SwingWrapper(shareChart).displayChart();
    }
}

/* Java遇到的问题：
1. 语法复杂，格式相关的废话很多，泛型搞死人
2. oop导致要记许多毫无意义的对象类型，比如 Table、ColumnType、XYchart和 SwingWrapper
3. 导入库太复杂，maven我搞了整整一天，最后还是用idea自带的导入
4. 缺少 data-analysis的优质库，对 dataframe的支持很差
5. 没有类似 Jupyter的 ide，IJava Kernel的 bug太多
5. tablesaw在任何方面都比不上 pandas，读取文件时每一字段都要规定类型，而且甚至不能选择行（pandas可以df.loc[index]，tablesaw只能用for-loop一个个找）
6. pandas和 matplotlib深度融合，可以直接 df.plot()，而 tablesaw内置的绘图只能以列为单位绘制，xchart太丑
*/